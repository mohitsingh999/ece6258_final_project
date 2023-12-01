
%% RUN BLSGSM Script
clear all;
warning('off','all')
% Testing will first happen on SIDD images.

% Load in the Ground Truth Images
sidd_image_path = 'D:\SIDD_Small_sRGB_Only\SIDD_Small_sRGB_Only\Data';

sidd_image_files = dir(fullfile(sidd_image_path, '**\*.*'));
sidd_image_files = sidd_image_files(~[sidd_image_files.isdir]);  %remove folders from list

n_files = length(sidd_image_files);  
j = 1;
%Perform BLSGSM Denoising on Each of the Images
for i=1:n_files
   % Check for Ground Truth Images, and Skip Running BLS-GSM on Those
   if strcmp(sidd_image_files(i).name, 'GT_SRGB_010.PNG')
       disp("Ground Truth. Skipping Processing")
       %gt_image =  im2gray(imread(strcat(cure_tsr_image_files(i).folder, '\', cure_tsr_image_files(i).name)));
       %gt_images{i} = imresize(gt_image, [256, 256]); %Store in struct for IQA Calculations
       continue
   end

   % Read in Image
   currentimage = imread(strcat(sidd_image_files(i).folder, '\', sidd_image_files(i).name));
   
   currentImage_gray = im2gray(currentimage);
   currentImage_gray = imresize(currentImage_gray, [256 256]);

   currentimage_n(:, :, 1) = imresize(currentimage(:, :, 1), [256 256]);
   currentimage_n(:, :, 2) = imresize(currentimage(:, :, 2), [256 256]);
   currentimage_n(:, :, 3) = imresize(currentimage(:, :, 3), [256 256]);

   % Perform BLSGSM Denoising (Color)
   denoisedImage(:, :, 1) = perform_blsgsm_denoising(currentimage_n(:, :, 1));
   denoisedImage(:, :, 2) = perform_blsgsm_denoising(currentimage_n(:, :, 2));
   denoisedImage(:, :, 3) = perform_blsgsm_denoising(currentimage_n(:, :, 3));

   % Perform BLSGSM Denoising (Gray)
   denoisedImage_gray = perform_blsgsm_denoising(currentImage_gray);

   % Find the Associated Ground Truth Image 
   gtImagedir = dir(strcat(sidd_image_files(i).folder, '\GT_SRGB_010.PNG'));
   %gtImage = im2gray(imread(strcat(gtImagedir.folder, '\', gtImagedir.name)));
   %gtImage = double(imresize(gtImage, [256, 256])); 

   gtImage = imread(strcat(gtImagedir.folder, '\', gtImagedir.name));
   gtImageColor(:, :, 1) = double(imresize(gtImage(:, :, 1), [256 256]));
   gtImageColor(:, :, 2) = double(imresize(gtImage(:, :, 2), [256 256]));
   gtImageColor(:, :, 3) = double(imresize(gtImage(:, :, 3), [256 256]));

   gtImage_gray = imresize(im2gray(gtImage), [256 256]);

   % Calculate the PSNR 
   currImage.psnr = psnr(denoisedImage, gtImageColor);

   % Calculate SSIM
   currImage.ssim = ssim(denoisedImage, gtImageColor);

   % Calculate CW-SSIM 
   currImage.cw_ssim = cw_ssim(denoisedImage_gray, gtImage_gray, 6, 16, 0, 0);

   % Calculate UNIQUE 
   currImage.unique = mslUNIQUE(denoisedImage, gtImageColor);

   % Calculate MSL-UNIQUE
   currImage.ms_unique = mslMSUNIQUE(denoisedImage, gtImageColor);

   % Calculate CSV
   currImage.csv = csv(denoisedImage, gtImageColor);

   % Calculate SUMMER
   currImage.summer = SUMMER(denoisedImage, gtImageColor);

   % Bundle Up Current Image Metadata
   currImage.name = sidd_image_files(i).name;
   currImage.folder = sidd_image_files(i).folder;

   IQA_CURE_TSR_Images{j} = currImage;

   % Display Progress To Test How Much Time is left
   progress = num2str(i/n_files * 100);
   disp(strcat('Progress : ', progress,  '%'));

   j = j + 1;

end

% Save Calculated IQA Metrics to a .mat file for later processing!
save('IQA_SIDDsRGB_BLSGSM.mat', 'IQA_CURE_TSR_Images')

