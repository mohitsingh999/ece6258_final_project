
%% RUN BLSGSM Script
clear all;
warning('off','all')
% Testing will first happen on CURE-OR images.

% Load in the Set 12 Images
set_12_image_path = 'C:\mohit\GT\ECE 6258\ece6258_final_project\datasets\set12\';

set_12_image_files = dir(fullfile(set_12_image_path, '**\*.*'));
set_12_image_files = set_12_image_files(~[set_12_image_files.isdir]);  %remove folders from list

n_files = length(set_12_image_files);  
j = 1;
k = 1;
%Perform BLSGSM Denoising on Each of the Images
for i=1:n_files

   % Check for Ground Truth Images, and Skip Running BLS-GSM on Those
   if contains(set_12_image_files(i).folder(13:length(set_12_image_files(i).folder)), 'GT')
       disp("Ground Truth. Skipping Processing")
       continue
   end

   % Read in Image
   currentimage = imread(strcat(set_12_image_files(i).folder, '\', set_12_image_files(i).name));
   
   currentimage_n(:, :, 1) = imresize(currentimage(:, :, 1), [256 256]);

   % Perform BLSGSM Denoising 
   denoisedImage(:, :, 1) = perform_blsgsm_denoising(currentimage_n(:, :, 1));

   denoisedImage_3(:, :, 1) = denoisedImage;
   denoisedImage_3(:, :, 2) = denoisedImage;
   denoisedImage_3(:, :, 3) = denoisedImage;

   % Find the Associated Ground Truth Image 
   gtFolder = 'C:\mohit\GT\ECE 6258\ece6258_final_project\datasets\set12\GT';
   gtImageName = set_12_image_files(i).name;

   gtImage = imread(strcat(gtFolder, '\', gtImageName));
   gtImage_gray = double(imresize(gtImage, [256 256]));

   gtImage_gray3(:, :, 1) = gtImage_gray;
   gtImage_gray3(:, :, 2) = gtImage_gray;
   gtImage_gray3(:, :, 3) = gtImage_gray;

   % Calculate the PSNR 
   currImage.psnr = psnr(denoisedImage, gtImage_gray);

   % Calculate SSIM
   currImage.ssim = ssim(denoisedImage, gtImage_gray);

   % Calculate CW-SSIM 
   currImage.cw_ssim = cw_ssim(denoisedImage, gtImage_gray, 6, 16, 0, 0);

   % Calculate UNIQUE 
   currImage.unique = mslUNIQUE(denoisedImage_3, gtImage_gray3);

   % Calculate MSL-UNIQUE
   currImage.ms_unique = mslMSUNIQUE(denoisedImage_3, gtImage_gray3);

   % Calculate CSV
   currImage.csv = csv(denoisedImage_3, gtImage_gray3);

   % Calculate SUMMER
   currImage.summer = SUMMER(denoisedImage_3, gtImage_gray3);

   % Bundle Up Current Image Metadata
   currImage.name = set_12_image_files(i).name;
   currImage.folder = set_12_image_files(i).folder;

   IQA_Set12_Images{j} = currImage;

   % Display Progress To Test How Much Time is left
   progress = num2str(i/n_files * 100);
   disp(strcat('Progress : ', progress,  '%'));

   j = j + 1;

end

% Save Calculated IQA Metrics to a .mat file for later processing!
save('IQA_Set12_BLSGSM.mat', 'IQA_Set12_Images')

