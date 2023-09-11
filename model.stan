
data {
  int<lower=0> N;  // number of observations
  int<lower=0> K;  // number of pitch types
  int<lower=0> P;  // number of pitchers
  int<lower=0> pitch_type[N];  // pitch type for each observation
  int<lower=0> pitcher[N];  // pitcher for each observation
  int<lower=0> stand[N];  // stand for each observation
  real balls[N];  // balls for each observation
  real strikes[N];  // strikes for each observation
  real observed_x[N];  // observed x for each observation
  real observed_z[N];  // observed z for each observation
}
parameters {
  real mu_x;
  real mu_z;
  real<lower=0> sigma_x;
  real<lower=0> sigma_z;
  real pitcher_mu_x[P];
  real pitcher_mu_z[P];
  real beta_stand_x;
  real beta_stand_z;
  real beta_pitch_type_x[K];
  real beta_pitch_type_z[K];
  real beta_balls_x;
  real beta_balls_z;
  real beta_strikes_x;
  real beta_strikes_z;
}
model {
  mu_x ~ normal(0, 2);
  mu_z ~ normal(0, 2);
  sigma_x ~ exponential(1);
  sigma_z ~ exponential(1);
  pitcher_mu_x ~ normal(mu_x, sigma_x);
  pitcher_mu_z ~ normal(mu_z, sigma_z);
  beta_stand_x ~ normal(0, 1);
  beta_stand_z ~ normal(0, 1);
  beta_pitch_type_x ~ normal(0, 1);
  beta_pitch_type_z ~ normal(0, 1);
  beta_balls_x ~ normal(0, 1);
  beta_balls_z ~ normal(0, 1);
  beta_strikes_x ~ normal(0, 1);
  beta_strikes_z ~ normal(0, 1);
  for (i in 1:N) {
    observed_x[i] ~ normal(pitcher_mu_x[pitcher[i]] + beta_stand_x * stand[i] + beta_pitch_type_x[pitch_type[i]] + beta_balls_x * balls[i] + beta_strikes_x * strikes[i], sigma_x);
    observed_z[i] ~ normal(pitcher_mu_z[pitcher[i]] + beta_stand_z * stand[i] + beta_pitch_type_z[pitch_type[i]] + beta_balls_z * balls[i] + beta_strikes_z * strikes[i], sigma_z);
  }
}
