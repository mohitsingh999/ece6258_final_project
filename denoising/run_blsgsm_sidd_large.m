
%% RUN BLSGSM Script
clear all;
warning('off','all')
% Testing will first happen on SIDD images.

% Load in the Ground Truth Images
sidd_image_path = 'D:\SIDD_Large\';

sidd_image_files = dir(fullfile(sidd_image_path, '**\*.*'));
sidd_image_files = sidd_image_files(~[sidd_image_files.isdir]);  %remove folders from list

n_files = length(sidd_image_files);  
j = 177;
k = 1;
%Perform BLSGSM Denoising on Each of the Images
for i=515:n_files
   % Skip the zip files
   if contains(sidd_image_files(i).name, '.zip')
       disp("zip file, skipping")
       continue
   end

   % Check for Ground Truth Images, and Skip Running BLS-GSM on Those
   if contains(sidd_image_files(i).name, 'GT')
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
   gtFolder = strrep(sidd_image_files(i).folder, 'NOISY', 'GT');
   gtImageName = strrep(sidd_image_files(i).name, 'NOISY', 'GT');

   %gtImagedir = dir(strcat(sidd_image_files(i).folder, '\GT_SRGB_010.PNG'));
   %gtImage = im2gray(imread(strcat(gtImagedir.folder, '\', gtImagedir.name)));
   %gtImage = double(imresize(gtImage, [256, 256])); 

   gtImage = imread(strcat(gtFolder, '\', gtImageName));
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

   IQA_SIDD_Large_Images{j} = currImage;

   % Display Progress To Test How Much Time is left
   progress = num2str(i/n_files * 100);
   disp(strcat('Progress : ', progress,  '%'));

   if progress == (200*k)/n_files * 100
       mat_name = strcat('IQA_SIDDsRGBLarge_BLSGSM', num2str(k*10), 'percent.mat');
       save(mat_name, 'IQA_SIDD_Large_Images')
       k = k + 1;
   end

   j = j + 1;

end

% Save Calculated IQA Metrics to a .mat file for later processing!
save('IQA_SIDDsRGBLarge_BLSGSM.mat', 'IQA_SIDD_Large_Images')

