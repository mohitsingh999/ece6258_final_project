
%% RUN BLSGSM Script
clear all;
warning('off','all')
% Testing will first happen on CURE-OR images.

% Load in the Ground Truth Images
cure_or_image_path = 'D:\CURE-OR\';

cure_or_image_files = dir(fullfile(cure_or_image_path, '**\*.*'));
cure_or_image_files = cure_or_image_files(~[cure_or_image_files.isdir]);  %remove folders from list

n_files = length(cure_or_image_files);  
j = 1;
k = 1;
%Perform BLSGSM Denoising on Each of the Images
for i=1:n_files
   % Skip the zip files
   if contains(cure_or_image_files(i).name, '.tar.gz')
       disp("zip file, skipping")
       continue
   end

   % Check for Ground Truth Images, and Skip Running BLS-GSM on Those
   if contains(cure_or_image_files(i).name, '_10_')
       disp("Ground Truth. Skipping Processing")
       %gt_image =  im2gray(imread(strcat(cure_tsr_image_files(i).folder, '\', cure_tsr_image_files(i).name)));
       %gt_images{i} = imresize(gt_image, [256, 256]); %Store in struct for IQA Calculations
       continue
   end

   % Read in Image
   currentimage = imread(strcat(cure_or_image_files(i).folder, '\', cure_or_image_files(i).name));
   
   %currentImage_gray = currentimage;
   %currentImage_gray = imresize(currentImage_gray, [256 256]);

   currentimage_n(:, :, 1) = imresize(currentimage(:, :, 1), [256 256]);
   %currentimage_n(:, :, 2) = imresize(currentimage(:, :, 2), [256 256]);
   %currentimage_n(:, :, 3) = imresize(currentimage(:, :, 3), [256 256]);

   % Perform BLSGSM Denoising (Color)
   denoisedImage(:, :, 1) = perform_blsgsm_denoising(currentimage_n(:, :, 1));
   %denoisedImage(:, :, 2) = perform_blsgsm_denoising(currentimage_n(:, :, 2));
   %denoisedImage(:, :, 3) = perform_blsgsm_denoising(currentimage_n(:, :, 3));

   denoisedImage_3(:, :, 1) = denoisedImage;
   denoisedImage_3(:, :, 2) = denoisedImage;
   denoisedImage_3(:, :, 3) = denoisedImage;


   % Perform BLSGSM Denoising (Gray)
   %denoisedImage_gray = perform_blsgsm_denoising(currentImage_gray);

   % Find the Associated Ground Truth Image 
   %gtFolder = 'D:\CURE-OR\10_grayscale_no_challenge';
   gtImageName = strrep(cure_or_image_files(i).name, cure_or_image_files(i).name(10:14), '_10_0');
   gtImagedir = dir(strcat('D:\CURE-OR\10_grayscale_no_challenge\**\', gtImageName));
   %gtImage = im2gray(imread(strcat(gtImagedir.folder, '\', gtImagedir.name)));
   %gtImage = double(imresize(gtImage, [256, 256])); 

   gtImage = imread(strcat(gtImagedir.folder, '\', gtImageName));
   %gtImageColor(:, :, 1) = double(imresize(gtImage(:, :, 1), [256 256]));
   %gtImageColor(:, :, 2) = double(imresize(gtImage(:, :, 2), [256 256]));
   %gtImageColor(:, :, 3) = double(imresize(gtImage(:, :, 3), [256 256]));

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
   currImage.name = cure_or_image_files(i).name;
   currImage.folder = cure_or_image_files(i).folder;

   IQA_CUREOR_Images{j} = currImage;

   % Display Progress To Test How Much Time is left
   progress = num2str(i/n_files * 100);
   disp(strcat('Progress : ', progress,  '%'));

   if progress == (20000*k)/n_files * 100
       mat_name = strcat('IQA_CUREOR_BLSGSM', num2str(k*10), 'percent.mat');
       save(mat_name, 'IQA_CUREOR_Images')
       k = k + 1;
   end

   j = j + 1;

end

% Save Calculated IQA Metrics to a .mat file for later processing!
save('IQA_CUREOR_BLSGSM.mat', 'IQA_CUREOR_Images')

