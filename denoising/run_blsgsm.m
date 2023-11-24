%% RUN BLSGSM Script
clear all;
warning('off','all')
% Testing will first happen on CURE-TSR images.

% Load in the Ground Truth Images
cure_tsr_image_path = 'D:\CURE-TSR\Real_Test\';

cure_tsr_image_files = dir(fullfile(cure_tsr_image_path, '**\*.*'));
cure_tsr_image_files = cure_tsr_image_files(~[cure_tsr_image_files.isdir]);  %remove folders from list

n_files = length(cure_tsr_image_files);  
j = 1;
%Perform BLSGSM Denoising on Each of the Images
for i=43181+38659:n_files
   curr_image_meta = strsplit(cure_tsr_image_files(i).name, '_');

   % Check for Ground Truth Images, and Skip Running BLS-GSM on Those
   if strcmp(curr_image_meta{1, 3}, '00')
       disp("Ground Truth. Skipping Processing")
       %gt_image =  im2gray(imread(strcat(cure_tsr_image_files(i).folder, '\', cure_tsr_image_files(i).name)));
       %gt_images{i} = imresize(gt_image, [256, 256]); %Store in struct for IQA Calculations
       continue
   end

   % Read in Image
   currentimage = imread(strcat(cure_tsr_image_files(i).folder, '\', cure_tsr_image_files(i).name));
   
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
   gtImagedir = dir(strcat(cure_tsr_image_path, 'ChallengeFree\',curr_image_meta{1, 1}, '_', curr_image_meta{1, 2}, '_', '*', curr_image_meta{1, 5}));
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
   currImage.name = cure_tsr_image_files(i).name;
   currImage.folder = cure_tsr_image_files(i).folder;

   IQA_CURE_TSR_Images{j} = currImage;

   % Display Progress To Test How Much Time is left
   progress = num2str(i/n_files * 100);
   disp(strcat('Progress : ', progress,  '%'));

   j = j + 1;

end

% Save Calculated IQA Metrics to a .mat file for later processing!
save('IQA_CURE_TSR.mat', 'IQA_CURE_TSR_Images')

