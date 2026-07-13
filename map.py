# interactive transfer prediction map, standalone script
# run with: python this_file.py, then open the printed localhost link
# click a source domain, then a target domain, model predicts transferability
# output is normalized 0-1 (0 lowest transferability, 1 highest), scaled against
# the full off-diagonal prediction range over all domains in the descriptors csv

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import xarray as xr
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from dash import Dash, dcc, html, Input, Output, State

# ---- config ----
MODEL_PATH = "training/transfer_model_v4.pt"
DESCRIPTORS_PATH = "encoder-inputs/domain_descriptions.csv"
DOMAIN_RASTER_PATH = "data/ecoregion_domains.zarr"  # assumed, matches visualize_domains.ipynb
HOLDOUT_IDS = [45, 46, 47, 49]  # excluded from scaler fit, same as training

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ---- model classes, copied from model_v4.ipynb, must match checkpoint exactly ----

class ModularEncoder(nn.Module):
    def __init__(self, atmospheric_idx, ground_idx, fire_idx, branch_embed_dim=3, dropout=0.2):
        super().__init__()
        self.atmospheric_idx = atmospheric_idx
        self.ground_idx = ground_idx
        self.fire_idx = fire_idx

        self.atmospheric_branch = self._make_branch(len(atmospheric_idx), branch_embed_dim, dropout)
        self.ground_branch = self._make_branch(len(ground_idx), branch_embed_dim, dropout)
        self.fire_branch = self._make_branch(len(fire_idx), branch_embed_dim, dropout)

    def _make_branch(self, input_dim, embed_dim, dropout):
        return nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(32, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(32, embed_dim)
        )

    def forward(self, x):
        x_atm = x[:, self.atmospheric_idx]
        x_ground = x[:, self.ground_idx]
        x_fire = x[:, self.fire_idx]

        e_atm = self.atmospheric_branch(x_atm)
        e_ground = self.ground_branch(x_ground)
        e_fire = self.fire_branch(x_fire)

        return torch.cat([e_atm, e_ground, e_fire], dim=-1)


class BiasHead(nn.Module):
    def __init__(self, input_dim=33, dropout=0.2):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(16, 2)
        )

    def forward(self, x):
        out = self.net(x)
        src_bias = out[:, 0]
        tgt_bias = out[:, 1]
        return src_bias, tgt_bias


class TransferModelV4(nn.Module):
    def __init__(self, atmospheric_idx, ground_idx, fire_idx, branch_embed_dim=3):
        super().__init__()
        self.encoder = ModularEncoder(atmospheric_idx, ground_idx, fire_idx, branch_embed_dim)
        self.bias_head = BiasHead(input_dim=33)

    def encode(self, x):
        e = self.encoder(x)
        src_bias, tgt_bias = self.bias_head(x)
        return e, src_bias, tgt_bias

    def forward(self, desc_i, desc_j):
        e_i, src_bias_i, _ = self.encode(desc_i)
        e_j, _, tgt_bias_j = self.encode(desc_j)

        dist_sq = ((e_i - e_j) ** 2).sum(dim=-1)
        pred = -dist_sq + src_bias_i + tgt_bias_j
        return pred, src_bias_i, tgt_bias_j


# ---- load descriptors, fit scaler same way as training ----

descriptors = pd.read_csv(DESCRIPTORS_PATH, index_col=0)
descriptors.index = descriptors.index.astype(int)

train_ids = [d for d in descriptors.index if d not in HOLDOUT_IDS]

scaler = StandardScaler()
scaler.fit(descriptors.loc[train_ids])

desc_scaled = pd.DataFrame(
    scaler.transform(descriptors),
    index=descriptors.index,
    columns=descriptors.columns
)

# branch column groups, same names as model_v4.ipynb
atmospheric_cols = ["vpd_mean", "vpd_std", "vpd_p90", "ws10_mean", "ws10_std", "ws10_p90",
                     "t2m_max_mean", "t2m_max_std", "t2m_max_p90", "tp_mean", "tp_std", "tp_p90"]
ground_cols = ["ndvi_mean", "ndvi_std", "ndvi_p90", "swvl1_mean", "swvl1_std", "swvl1_p90",
               "swvl4_mean", "swvl4_std", "swvl4_p90", "land_cover_diversity"]
fire_cols = ["fwi_mean_mean", "fwi_mean_std", "fwi_mean_p90", "gwis_ba_mean", "gwis_ba_std", "gwis_ba_p90",
             "cams_frpfire_mean", "cams_frpfire_std", "cams_frpfire_p90", "fire_sparsity", "fire_season_length"]

atmospheric_idx = [desc_scaled.columns.get_loc(c) for c in atmospheric_cols]
ground_idx = [desc_scaled.columns.get_loc(c) for c in ground_cols]
fire_idx = [desc_scaled.columns.get_loc(c) for c in fire_cols]

# ---- load model ----

model = TransferModelV4(atmospheric_idx, ground_idx, fire_idx, branch_embed_dim=3).to(device)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.eval()


def raw_predict(source_id, target_id):
    # source_id plays i, target_id plays j, asymmetric like training
    with torch.no_grad():
        di = torch.tensor(desc_scaled.loc[source_id].values, dtype=torch.float32).unsqueeze(0).to(device)
        dj = torch.tensor(desc_scaled.loc[target_id].values, dtype=torch.float32).unsqueeze(0).to(device)
        pred, _, _ = model(di, dj)
    return pred.item()


# ---- precompute prediction range for normalization ----
# runs the full pairwise matrix once over every domain in the descriptors csv,
# min/max taken off-diagonal only since self-pairs score artificially high
# and would compress the rest of the range toward 0

all_ids = desc_scaled.index.tolist()
pair_i = [i for i in all_ids for j in all_ids]
pair_j = [j for i in all_ids for j in all_ids]

with torch.no_grad():
    desc_i_tensor = torch.tensor(desc_scaled.loc[pair_i].values, dtype=torch.float32).to(device)
    desc_j_tensor = torch.tensor(desc_scaled.loc[pair_j].values, dtype=torch.float32).to(device)
    full_preds, _, _ = model(desc_i_tensor, desc_j_tensor)
    full_preds = full_preds.cpu().numpy()

off_diag_mask = np.array([i != j for i, j in zip(pair_i, pair_j)])
PRED_MIN = full_preds[off_diag_mask].min()
PRED_MAX = full_preds[off_diag_mask].max()

print(f"prediction range used for normalization: min {PRED_MIN:.4f}, max {PRED_MAX:.4f}")


def predict_transfer(source_id, target_id):
    # returns predicted transferability normalized 0-1, 0 lowest, 1 highest
    raw = raw_predict(source_id, target_id)
    norm = (raw - PRED_MIN) / (PRED_MAX - PRED_MIN)
    return float(np.clip(norm, 0.0, 1.0))


# ---- load domain raster for the map ----

regimes = xr.open_zarr(DOMAIN_RASTER_PATH, consolidated=True)
domain_da = regimes["domain_id"]
domain_grid = domain_da.values.astype(int)

dims = domain_da.dims  # should be a 2-tuple, (lat-like dim, lon-like dim)

lat_names = ["lat", "latitude", "y"]
lon_names = ["lon", "longitude", "x"]

lat_dim = next(d for d in dims if d in lat_names)
lon_dim = next(d for d in dims if d in lon_names)

lat_vals = domain_da.coords[lat_dim].values
lon_vals = domain_da.coords[lon_dim].values

modeled_ids = set(desc_scaled.index)
lon_mesh, lat_mesh = np.meshgrid(lon_vals, lat_vals)


def domain_centroid(domain_id):
    mask = domain_grid == domain_id
    return lon_mesh[mask].mean(), lat_mesh[mask].mean()


def base_figure():
    z = domain_grid.astype(float)
    z[z == -1] = np.nan  # ocean / fill value

    fig = go.Figure()
    fig.add_trace(go.Heatmap(
        z=z, x=lon_vals, y=lat_vals,
        colorscale="Viridis", showscale=False, hoverinfo="none"
    ))
    fig.add_trace(go.Scattergl(x=[], y=[], mode="markers+text",
                                marker=dict(size=14, color="red"),
                                text=[], textposition="top center", showlegend=False))
    fig.update_layout(
        title="click a source domain, then a target domain",
        xaxis_title="longitude", yaxis_title="latitude",
        height=650, margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig


# ---- dash app ----

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="map", figure=base_figure()),
    dcc.Store(id="selected-domains", data=[]),  # holds up to 2 domain ids between callbacks
])


@app.callback(
    Output("map", "figure"),
    Output("selected-domains", "data"),
    Input("map", "clickData"),
    State("selected-domains", "data"),
)
def handle_click(click_data, selected):
    if click_data is None:
        return base_figure(), selected

    click_lon = click_data["points"][0]["x"]
    click_lat = click_data["points"][0]["y"]
    lon_idx = int(np.argmin(np.abs(lon_vals - click_lon)))
    lat_idx = int(np.argmin(np.abs(lat_vals - click_lat)))
    domain_id = int(domain_grid[lat_idx, lon_idx])

    fig = base_figure()

    if domain_id == -1:
        fig.update_layout(title="clicked ocean/no domain, try again")
        return fig, selected

    if domain_id not in modeled_ids:
        fig.update_layout(title=f"domain {domain_id} has no descriptors, not modeled")
        return fig, selected

    # third click resets and starts a new pair
    if len(selected) >= 2:
        selected = []

    selected = selected + [domain_id]

    xs, ys, labels = [], [], []
    for idx, d in enumerate(selected):
        lon, lat = domain_centroid(d)
        xs.append(lon)
        ys.append(lat)
        labels.append("source" if idx == 0 else "target")
    fig.data[1].x = xs
    fig.data[1].y = ys
    fig.data[1].text = labels

    if len(selected) == 1:
        fig.update_layout(title=f"source domain {selected[0]} selected, click a target domain")
    else:
        src, tgt = selected
        score = predict_transfer(src, tgt)
        fig.update_layout(title=f"predicted transfer {src} -> {tgt}: {score:.2f} (0-1 scale)")

    return fig, selected


if __name__ == "__main__":
    app.run(debug=True)