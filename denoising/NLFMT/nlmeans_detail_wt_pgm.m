%%% Image Denoising using NL means Filter and Method Noise Wavelet Thresholding.
%%% Author : B.K. SHREYAMSHA KUMAR 

%%% Copyright (c) 2012 B. K. Shreyamsha Kumar 
%%% All rights reserved.
 
%%% Permission is hereby granted, without written agreement and without license or royalty fees, to use, copy, 
%%% modify, and distribute this code (the source files) and its documentation for any purpose, provided that the 
%%% copyright notice in its entirety appear in all copies of this code, and the original source of this code, 
%%% This should be acknowledged in any publication that reports research using this code. The research is to be 
%%% cited in the bibliography as:

%%% B. K. Shreyamsha Kumar, “Image Denoising based on Non Local-means Filter and its Method Noise Thresholding”, 
%%% Signal, Image and Video Processing, pp. 1-17, 2012. (doi: 10.1007/s11760-012-0389-y)


close all;
clear;
clc;

%%% NL-means Filter Parameters.
ksize=7;    %%% Neighbor Window Size (should be odd).7
ssize=21;   %%% Search Window Size (should be odd).21
sigmas=5;   %%% Sigma for Gaussian Kernel Generation.5

%%% Wavelet Transform Parameters.
Nlevels=3;
NoOfBands=3*Nlevels+1;
wname='db8'; %% db8 sym8 db16 coif5 bior6.8
sorh='s'; % s or h or t -> trimmed

x = imread('/media/nwitt/Seagate Portable Drive/6258 Project/cureor/mini/train/01950.jpg');
% x = imread('lena512.jpg');
% x = imread('Barbara512.png');
% x = imread('boat512.jpg');
% x = imread('baboon512.jpg');

if(size(x,3)==3)
    x=rgb2gray(x);
end
[M,N]=size(x);

%%% Gaussian Noise addition.
mean_val=0;
noise_std=20; %% 10,20,30,40,50.
sizeA = size(x);
randn('seed',212096); %%% Results depend on 'seed' of the random noise.
xn = double(x) + (noise_std*randn(sizeA)) + mean_val;
xn = max(0,min(xn,255));

%%% PSNR Computation of Noisy Image.
xn_mse=sum(sum((double(x)-double(xn)).^2))/(M*N);
xn_psnr=10*log10(255^2./xn_mse);

%%% Noise Level Estimation using Robust Median Estimator.
if(isequal(wname,'DCHWT'))
   dchw=dchwtf2(xn,1);
   tt1=dchw{1}(:)';
else 
   [ca,ch,cv,cd]=dwt2(xn,wname);
   tt1=cd(:)';
end
median_hh2=median(abs(tt1)); %% HH1->Subband containing finest level diagonal details.
std_dev2=(median_hh2/0.6745);

%%% NL-means Filtering.
tic
im_nl=nlmeans_filt2D(xn,sigmas,ksize,ssize,std_dev2);
toc
yd=double(xn)-im_nl;

%%% General Wavelet Decomposition.
dwtmode('per');
[C,S]=wavedec2(yd,Nlevels,wname);
k=NoOfBands;
CW{k}=reshape(C(1:S(1,1)*S(1,2)),S(1,1),S(1,2));
k=k-1;
st_pt=S(1,1)*S(1,2);
for i=2:size(S,1)-1
   slen=S(i,1)*S(i,2);
   CW{k}=reshape(C(st_pt+slen+1:st_pt+2*slen),S(i,1),S(i,2));  %% Vertical
   CW{k-1}=reshape(C(st_pt+1:st_pt+slen),S(i,1),S(i,2));   %% Horizontal
   CW{k-2}=reshape(C(st_pt+2*slen+1:st_pt+3*slen),S(i,1),S(i,2));  %% Diagonal
   st_pt=st_pt+3*slen;
   k=k-3;
end

%%%% BayesShrink Technique.
tt2=CW{1}(:)';
median_hh2=median(abs(tt2)); %% HH1->Subband containing finest level diagonal details.
std_dev2=(median_hh2/0.6745);
cw_noise_var=std_dev2^2; %% var=std^2

for i=1:NoOfBands-1
    thr = bayesthf(CW{i},cw_noise_var);
    yw{i} = threshf(CW{i},sorh,thr,2);    
end
yw{i+1}=CW{i+1};

%%% General Wavelet Reconstruction.
k=NoOfBands;
xrtemp=reshape(yw{k},1,S(1,1)*S(1,2));
k=k-1;
for i=2:size(S,1)-1
   xrtemp=[xrtemp reshape(yw{k-1},1,S(i,1)*S(i,2)) reshape(yw{k},1,S(i,1)*S(i,2)) reshape(yw{k-2},1,S(i,1)*S(i,2))];
   k=k-3;
end
ydr=(waverec2(xrtemp,S,wname));
nl_mnt=im_nl+ydr;
nl_mnt8=uint8(nl_mnt);

toc

%%%% MSE Computation.
ynl_mse=sum(sum((double(x)-double(im_nl)).^2))/(M*N);
ynl_mnt_mse=sum(sum((double(x)-double(nl_mnt8)).^2))/(M*N);

%%%% PSNR Computation.
wname,noise_std,xn_psnr
psnr_nl=10*log10(255^2./ynl_mse);
psnr_nl_mnt=10*log10(255^2./ynl_mnt_mse);
psnr_nl_mnt-psnr_nl;


%%%% Image Quality Index (IQI) Computation.
mean_org=mean(x(:));
var_org=sum((x(:)-mean_org).^2)/(M*N-1);

%%%% IQI for NL-means Filter.
im_nl8=uint8(im_nl);
mean_nl=mean(im_nl8(:));
var_nl=sum((im_nl8(:)-mean_nl).^2)/(M*N-1);
cross_var_wt=sum((x(:)-mean_org).*(im_nl8(:)-mean_nl))/(M*N-1);
IQI_nl=(4*cross_var_wt*mean_org*mean_nl)/((var_org+var_nl)*(mean_org^2+mean_nl^2));

%%%% IQI for NL-means & its Method Noise Thresholding.
mean_nl_mnt=mean(nl_mnt8(:));
var_nl_mnt=sum((nl_mnt8(:)-mean_nl_mnt).^2)/(M*N-1);
cross_var_wt=sum((x(:)-mean_org).*(nl_mnt8(:)-mean_nl_mnt))/(M*N-1);
IQI_nl_mnt=(4*cross_var_wt*mean_org*mean_nl_mnt)/((var_org+var_nl_mnt)*(mean_org^2+mean_nl_mnt^2));

%%%% Visual Fidelity Index (VIF) Computation.
vif_nl = vifvec(double(x),im_nl);
% vif_nl = vifvec(double(x),im_nl8) %%% uint8.
vif_nl_mnt = vifvec(double(x),nl_mnt);

vif_nl,psnr_nl,IQI_nl
vif_nl_mnt,psnr_nl_mnt,IQI_nl_mnt

% %%% Denoised Image Plots
% figure,imshow(uint8(x)),colormap gray
% figure,imshow(uint8(xn)),colormap gray

figure,imshow(uint8(im_nl)),colormap gray,title('NL-means Filtering');
figure,imshow(nl_mnt8),colormap gray,title('NL-means Filtering & Method Noise Thresholding');

%%% Method Noise Plots;
mn=xn-double(x);
mn_nl=yd;
mn_nl_mnt=xn-double(nl_mnt8);
% figure,imshow(mn_nl),colormap gray,title('Method Noise --> NL-means Filtering');
% figure,imshow(mn_nl_mnt),colormap gray,title('Method Noise --> NL-means Filtering & Method Noise Thresholding');
