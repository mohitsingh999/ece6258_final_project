close all;
clear;
clc;

addpath("NLFMT");

%%% NL-means Filter Parameters.
ksize=7;    %%% Neighbor Window Size (should be odd).7
ssize=21;   %%% Search Window Size (should be odd).21
sigmas=5;   %%% Sigma for Gaussian Kernel Generation.5

%%% Wavelet Transform Parameters.
Nlevels=3;
NoOfBands=3*Nlevels+1;
wname='db8'; %% db8 sym8 db16 coif5 bior6.8
sorh='s'; % s or h or t -> trimmed

% x = imread('/media/nwitt/Seagate Portable Drive/6258 Project/cureor/mini/train/01950.jpg');
x = imread('../images/cure-or-guassian-blur/01950.jpg');

if(size(x,3)==3)
    x=rgb2gray(x);
end
[M,N]=size(x);

%%% Noise Level Estimation using Robust Median Estimator.
if(isequal(wname,'DCHWT'))
   dchw=dchwtf2(x,1);
   tt1=dchw{1}(:)';
else 
   [ca,ch,cv,cd]=dwt2(x,wname);
   tt1=cd(:)';
end
median_hh2=median(abs(tt1)); %% HH1->Subband containing finest level diagonal details.
std_dev2=(median_hh2/0.6745);

%%% NL-means Filtering.
tic
im_nl=nlmeans_filt2D(x,sigmas,ksize,ssize,std_dev2);
toc
% yd=double(x)-im_nl;

save("data/01950_nlm.mat", im_nl)
imshow(im_nl)

