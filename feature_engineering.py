def compute_approach_angles(df):
    import numpy as np
    yf = 17/12
    df['vy_f'] = -np.sqrt(df['vy0']**2 - (2 * df['ay'] * (50 - yf)))
    df['t'] = (df['vy_f'] - df['vy0']) / df['ay']
    df['vz_f'] = df['vz0'] + (df['az'] * df['t'])
    df['vx_f'] = df['vx0'] + (df['ax'] * df['t'])

    df['vaa'] = -np.arctan(df['vz_f']/df['vy_f']) * (180 / np.pi)
    df['haa'] = np.arctan(df['vx_f']/df['vy_f']) * (180 / np.pi)

    df['vaa2'] = np.arctan((2.5 - df['release_pos_z']) / (df['release_pos_y'])) * (180 / np.pi)
    df['haa2'] = np.arctan((0 - df['release_pos_x']) / (df['release_pos_y'])) * (180 / np.pi)
    return df

def compute_adjusted_axis_deviation(df):
    import numpy as np
    df['axis_deviation_adj'] = np.where(df['p_throws']=='L', df['diff_measured_inferred'].mul(-1), df['diff_measured_inferred'])
    return df

def compute_fastball_relative_features(df):
    import numpy as np
    fastball_metrics = df.groupby(['player_name', 'pitcher', 'game_pk', 'pitch_type'])[['release_speed', 'hawkeye_measured', 'active_spin_formatted', 'pfx_x', 'pfx_z', 'vaa', 'haa']].mean().round().reset_index()
    fastball_metrics = fastball_metrics.rename(columns={
        'release_speed': 'avg_top_velocity',
        'hawkeye_measured':'fb_spin_axis',
        'active_spin_formatted':'fb_active_spin',
        'az':'fastball_vert',
        'ax':'fastball_horz',
        'vaa':'fastball_vaa',
        'haa':'fastball_haa'})


    fastball_metrics = fastball_metrics.dropna()
    idx = fastball_metrics.groupby(['pitcher', 'game_pk'])['avg_top_velocity'].idxmax()
    fastball_metrics_max_velocity = fastball_metrics.loc[idx].rename(columns={'pitch_type':'top_velo_pitch_type'})

    df = df.merge(fastball_metrics_max_velocity, on=['player_name', 'pitcher', 'game_pk'], how='left')

    df['velo_delta'] = df['avg_top_velocity'] - df['release_speed']
    df['spin_axis_delta'] = np.abs(df['hawkeye_measured'] - df['fb_spin_axis'])

    df['vert_delta'] = np.abs(df['fastball_vert'] - df['pfx_z'])
    df['horz_delta'] = np.abs(df['fastball_horz'] - df['pfx_x'])

    return df