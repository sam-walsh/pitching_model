def compute_fastball_relative_features(df):
    fastball_metrics = df.groupby(['player_name', 'pitcher', 'game_pk', 'pitch_type'])[['release_speed', 'hawkeye_measured', 'active_spin_formatted', 'az', 'ax']].mean().round().reset_index()
    fastball_metrics = fastball_metrics.rename(columns={
        'release_speed': 'avg_top_velocity',
        'hawkeye_measured':'fb_spin_axis',
        'active_spin_formatted':'fb_active_spin',
        'az':'fastball_vert',
        'ax':'fastball_horz'})

    fastball_metrics = fastball_metrics.dropna()
    idx = fastball_metrics.groupby(['pitcher', 'game_pk'])['avg_top_velocity'].idxmax()
    fastball_metrics_max_velocity = fastball_metrics.loc[idx].rename(columns={'pitch_type':'top_velo_pitch_type'})

    df = df.merge(fastball_metrics_max_velocity, on=['player_name', 'pitcher', 'game_pk'], how='left')

    df['velo_delta'] = df['avg_top_velocity'] - df['release_speed']
    df['spin_axis_delta'] = df['hawkeye_measured'] - df['fb_spin_axis']

    df['vert_delta'] = df['fastball_vert'] - df['az']
    df['horz_delta'] = df['fastball_horz'] - df['ax']

    return df

def compute_approach_angles(df):
    import numpy as np
    df['vaa'] = np.arctan((df['plate_z'] - df['release_pos_z']) / (df['release_pos_y'])) * (180 / np.pi)
    df['haa'] = np.arctan((df['plate_x'] - df['release_pos_x']) / (df['release_pos_y'])) * (180 / np.pi)
    return df

def compute_adjusted_axis_deviation(df):
    import numpy as np
    df['axis_deviation_adj'] = np.where(df['p_throws']=='L', df['diff_measured_inferred'].mul(-1), df['diff_measured_inferred'])
    return df