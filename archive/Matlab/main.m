%%
% Yifei Wang Nov.13.2024
clear
clc

%%
Solar_data = readtable('../Dataset/solar_data.csv');
Site_params = readtable('../Dataset/site_params.csv');

site_1_para = Site_params(1,:)
site_2_para = Site_params(2,:)
site_3_para = Site_params(3,:)
site_4_para = Site_params(4,:)
%% Solar_data visualisation
% Split Solar_data by the first column values (1, 2, 3, 4)
solar_data_1 = Solar_data(Solar_data{:,1} == 1, :);
solar_data_2 = Solar_data(Solar_data{:,1} == 2, :);
solar_data_3 = Solar_data(Solar_data{:,1} == 3, :);
solar_data_4 = Solar_data(Solar_data{:,1} == 4, :);
%%
plot(solar_data_1{1:100,2},solar_data_1{1:100,3})
