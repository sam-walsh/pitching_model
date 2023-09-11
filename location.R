library(tidyverse)
library(rstan)
setwd("C:/Users/wampl/pitching_model")
options(mc.cores = parallel::detectCores())
rstan_options(auto_write = TRUE)
rstan_options(threads_per_chain = 1)

data <- read_csv('statcast_data/2023.csv')

pitcher_counts <- data %>% count(pitcher)
data <- data %>% filter(pitcher %in% pitcher_counts$pitcher[pitcher_counts$n > 100])
data <- data %>% filter(pitch_type %in% c('FF'))

set.seed(123) # for reproducibility
data <- data %>% sample_n(10000)

data$stand <- as.integer(data$stand == 'L')
data$pitch_type <- as.integer(as.factor(data$pitch_type))

data <- data %>% select(pitcher, plate_x, plate_z, stand, pitch_type, balls, strikes)

data <- data %>% drop_na()

num_pitchers <- n_distinct(data$pitcher)
pitcher_idx <- as.integer(as.factor(data$pitcher))
num_pitch_types <- n_distinct(data$pitch_type)
stand <- data$stand
balls <- data$balls
strikes <- data$strikes
observed_x <- data$plate_x
observed_z <- data$plate_z
obs_sd_x <- sd(observed_x, na.rm = TRUE)
obs_sd_z <- sd(observed_z, na.rm = TRUE)

# Compile and run Stan model
model <- rstan::stan_model(file = 'model.stan')

# Prepare data for Stan model
data_list <- list(
  N = nrow(data),
  K = num_pitch_types,
  P = num_pitchers,
  pitch_type = data$pitch_type + 1,
  pitcher = pitcher_idx + 1,
  stand = stand,
  balls = balls,
  strikes = strikes,
  observed_x = observed_x,
  observed_z = observed_z
)

# Sample from the model
fit <- rstan::sampling(model, data = data_list, iter = 500, verbose=TRUE, chains=1, cores=1)

# Print summary of the fit
print(summary(fit))
