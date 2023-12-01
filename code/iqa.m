function iqa(image_path, image_ref_path, image_id, result_file)
    image_path = string(image_path);
    image_ref_path = string(image_ref_path);

    addpath("../IQA_Metrics/CSV/Code/");
    addpath("../IQA_Metrics/CSV/Code/FastEMD");
    addpath("../IQA_Metrics/MS-UNIQUE/");
    addpath("../IQA_Metrics/MS-UNIQUE/InputWeights");
    addpath("../IQA_Metrics/SUMMER/Code/");
    addpath("../IQA_Metrics/UNIQUE-Unsupervised-Image-Quality-Estimation/");
    addpath("../IQA_Metrics/UNIQUE-Unsupervised-Image-Quality-Estimation/InputWeights/");
    addpath("../IQA_Metrics/matlabPyrTools-master/");
    addpath("../IQA_Metrics/matlabPyrTools-master/MEX");

    % Load in both images
    if image_path.contains(".MAT")
        load(image_path);
        image = x;
    else
        image = imread(image_path);
    end
    if image_ref_path.contains(".MAT")
        load(image_ref_path);
        image_ref = x;
    else
        image_ref = imread(image_ref_path);
    end

    % Convert to gray if necessary
    if length(size(image)) == 3
        image_gray = rgb2gray(image);
        image_rgb = image;
    else
        image_gray = image;
        image_rgb = cat(3, image, image, image);
    end
    if length(size(image_ref)) == 3
        image_ref_gray = rgb2gray(image_ref);
        image_ref_rgb = image_ref;
    else
        image_ref_gray = image_ref;
        image_ref_rgb = cat(3, image_ref, image_ref, image_ref);
    end

    try
        % Calculate the PSNR
        % 0.25 seconds
        psnr_val = psnr(image, image_ref);
    catch
        psnr_val = 0.0;
    end

    try
        % Calculate SSIM
        % 3.42 seconds
        ssim_val = ssim(image, image_ref);
    catch
        ssim_val = 0;
    end

    try
        % Calculate CW-SSIM 
        % LONG
        cw_ssim_val = cw_ssim(image_gray, image_ref_gray, 6, 16, 0, 0);
    catch
        cw_ssim_val = 0;
    end

    try
        % Calculate UNIQUE 
        % 8 seconds
        unique_val = mslUNIQUE(image_rgb, image_ref_rgb);
    catch
        unique_val = 0;
    end

    try
        % Calculate MS-UNIQUE
        % 27 seconds
        ms_unique_val = mslMSUNIQUE(image_rgb, image_ref_rgb);
    catch
        ms_unique_val = 0;
    end

    try
        % Calculate CSV
        % 13 seconds
        csv_val = csv(image_rgb, image_ref_rgb);
    catch
        csv_val = 0;
    end

    try
        % Calculate SUMMER
        % 1 second
        summer_val = SUMMER(image_rgb, image_ref_rgb);
    catch
        summer_val = 0;
    end

    % Open a file for writing
    fileID = fopen(result_file, 'a');

    % Format and write the data to the file
    fprintf(fileID, '%s %.3f %.3f %.3f %.3f %.3f %.3f %.3f\r\n', image_id, psnr_val, ssim_val, cw_ssim_val, unique_val, ms_unique_val, csv_val, summer_val);

    % Close the file
    fclose(fileID);
end
