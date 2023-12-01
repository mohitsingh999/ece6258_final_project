%% Evaluate BLSGSM IQA Outputs
% Go Dataset by dataset 

% CURE-TSR Results Evaluation
load('IQA_CURE_TSR_20percent.mat');

avg_psnr_cure_tsr = 0;
avg_ssim_cure_tsr = 0;
avg_cw_ssim_cure_tsr = 0;
avg_unique_cure_tsr = 0;
avg_msunique_cure_tsr = 0;
avg_csv_cure_tsr = 0;
avg_summer_cure_tsr = 0;

avg_psnr_decolorization = 0;
avg_psnr_decolorization_count = 0;
avg_psnr_lens_blur = 0;
avg_psnr_lens_blur_count = 0;
avg_psnr_codec = 0;
avg_psnr_codec_count = 0;
avg_psnr_darkening = 0;
avg_psnr_darkening_count = 0;


avg_psnr_level1 = 0;
avg_psnr_level1_count = 0;
avg_psnr_level2 = 0;
avg_psnr_level2_count = 0;
avg_psnr_level3 = 0;
avg_psnr_level3_count = 0;
avg_psnr_level4 = 0;
avg_psnr_level4_count = 0;
avg_psnr_level5 = 0;
avg_psnr_level5_count = 0;


for i = 1:length(IQA_CURE_TSR_Images)

    % Parse the name
    name = split(IQA_CURE_TSR_Images{i}.name, '_');

    if strcmp(name(3), '01')
        avg_psnr_decolorization = avg_psnr_decolorization + IQA_CURE_TSR_Images{i}.psnr;
        avg_psnr_decolorization_count = avg_psnr_decolorization_count + 1;
    end

    if strcmp(name(3), '02')
        avg_psnr_lens_blur = avg_psnr_lens_blur + IQA_CURE_TSR_Images{i}.psnr;
        avg_psnr_lens_blur_count = avg_psnr_lens_blur_count + 1;
    end

    if strcmp(name(3), '03')
        avg_psnr_codec = avg_psnr_codec + IQA_CURE_TSR_Images{i}.psnr;
        avg_psnr_codec_count = avg_psnr_codec_count + 1;
    end

    if strcmp(name(3), '04')
        avg_psnr_darkening = avg_psnr_darkening + IQA_CURE_TSR_Images{i}.psnr;
        avg_psnr_darkening_count = avg_psnr_darkening_count + 1;
    end

    if strcmp(name(4), '01')
        avg_psnr_level1 = avg_psnr_level1 + IQA_CURE_TSR_Images{i}.psnr;
        avg_psnr_level1_count = avg_psnr_level1_count + 1;
    end

    if strcmp(name(4), '02')
        avg_psnr_level2 = avg_psnr_level2 + IQA_CURE_TSR_Images{i}.psnr;
        avg_psnr_level2_count = avg_psnr_level2_count + 1;
    end

    if strcmp(name(4), '03')
        avg_psnr_level3 = avg_psnr_level3 + IQA_CURE_TSR_Images{i}.psnr;
        avg_psnr_level3_count = avg_psnr_level3_count + 1;
    end

    if strcmp(name(4), '04')
        avg_psnr_level4 = avg_psnr_level4 + IQA_CURE_TSR_Images{i}.psnr;
        avg_psnr_level4_count = avg_psnr_level4_count + 1;
    end

    if strcmp(name(4), '05')
        avg_psnr_level5 = avg_psnr_level5 + IQA_CURE_TSR_Images{i}.psnr;
        avg_psnr_level5_count = avg_psnr_level5_count + 1;
    end

    avg_psnr_cure_tsr = avg_psnr_cure_tsr + IQA_CURE_TSR_Images{i}.psnr;
    avg_ssim_cure_tsr = avg_ssim_cure_tsr + IQA_CURE_TSR_Images{i}.ssim;
    avg_cw_ssim_cure_tsr = avg_cw_ssim_cure_tsr + IQA_CURE_TSR_Images{i}.cw_ssim;
    avg_unique_cure_tsr = avg_unique_cure_tsr + IQA_CURE_TSR_Images{i}.unique;
    avg_msunique_cure_tsr = avg_msunique_cure_tsr + IQA_CURE_TSR_Images{i}.ms_unique;
    avg_csv_cure_tsr = avg_csv_cure_tsr + IQA_CURE_TSR_Images{i}.csv;
    avg_summer_cure_tsr = avg_summer_cure_tsr + IQA_CURE_TSR_Images{i}.summer;

end

avg_psnr_cure_tsr = avg_psnr_cure_tsr / length(IQA_CURE_TSR_Images);
avg_ssim_cure_tsr = avg_ssim_cure_tsr / length(IQA_CURE_TSR_Images);
avg_cw_ssim_cure_tsr = avg_cw_ssim_cure_tsr / length(IQA_CURE_TSR_Images);
avg_unique_cure_tsr = avg_unique_cure_tsr / length(IQA_CURE_TSR_Images);
avg_msunique_cure_tsr = avg_msunique_cure_tsr / length(IQA_CURE_TSR_Images);
avg_csv_cure_tsr = avg_csv_cure_tsr / length(IQA_CURE_TSR_Images);
avg_summer_cure_tsr = avg_summer_cure_tsr / length(IQA_CURE_TSR_Images);

avg_psnr_darkening = avg_psnr_darkening / avg_psnr_darkening_count;
avg_psnr_codec = avg_psnr_codec / avg_psnr_codec_count;
avg_psnr_decolorization = avg_psnr_decolorization / avg_psnr_decolorization_count;

avg_psnr_level1 = avg_psnr_level1 / avg_psnr_level1_count;
avg_psnr_level2 = avg_psnr_level2 / avg_psnr_level2_count;
avg_psnr_level3 = avg_psnr_level3 / avg_psnr_level3_count;
avg_psnr_level4 = avg_psnr_level4 / avg_psnr_level4_count;
avg_psnr_level5 = avg_psnr_level5 / avg_psnr_level5_count;

% SIDD Results Evaluation 
avg_psnr_sidd = 0;
avg_ssim_sidd = 0;
avg_cw_ssim_sidd = 0;
avg_unique_sidd = 0;
avg_msunique_sidd = 0;
avg_csv_sidd = 0;
avg_summer_sidd = 0;

load('IQA_SIDDsRGB_BLSGSM.mat');

for i = 1:length(IQA_CURE_TSR_Images)
    avg_psnr_sidd = avg_psnr_sidd + IQA_CURE_TSR_Images{i}.psnr;
    avg_ssim_sidd = avg_ssim_sidd + IQA_CURE_TSR_Images{i}.ssim;
    avg_cw_ssim_sidd = avg_cw_ssim_sidd + IQA_CURE_TSR_Images{i}.cw_ssim;
    avg_unique_sidd = avg_unique_sidd + IQA_CURE_TSR_Images{i}.unique;
    avg_msunique_sidd = avg_msunique_sidd + IQA_CURE_TSR_Images{i}.ms_unique;
    avg_csv_sidd = avg_csv_sidd + IQA_CURE_TSR_Images{i}.csv;
    avg_summer_sidd = avg_summer_sidd + IQA_CURE_TSR_Images{i}.summer;
end
avg_psnr_sidd = avg_psnr_sidd / length(IQA_CURE_TSR_Images);
avg_ssim_sidd = avg_ssim_sidd / length(IQA_CURE_TSR_Images);
avg_cw_ssim_sidd = avg_cw_ssim_sidd / length(IQA_CURE_TSR_Images);
avg_unique_sidd = avg_unique_sidd / length(IQA_CURE_TSR_Images);
avg_msunique_sidd = avg_msunique_sidd / length(IQA_CURE_TSR_Images);
avg_csv_sidd = avg_csv_sidd / length(IQA_CURE_TSR_Images);
avg_summer_sidd = avg_summer_sidd / length(IQA_CURE_TSR_Images);

% Set-12 Results Evaluation 
avg_psnr_set12 = 0;
avg_ssim_set12 = 0;
avg_cw_ssim_set12 = 0;
avg_unique_set12 = 0;
avg_msunique_set12 = 0;
avg_csv_set12 = 0;
avg_summer_set12 = 0;

load('IQA_Set12_BLSGSM.mat');

for i = 1:length(IQA_Set12_Images)
    avg_psnr_set12 = avg_psnr_set12 + IQA_Set12_Images{i}.psnr;
    avg_ssim_set12 = avg_ssim_set12 + IQA_Set12_Images{i}.ssim;
    avg_cw_ssim_set12 = avg_cw_ssim_set12 + IQA_Set12_Images{i}.cw_ssim;
    avg_unique_set12 = avg_unique_set12 + IQA_Set12_Images{i}.unique;
    avg_msunique_set12 = avg_msunique_set12 + IQA_Set12_Images{i}.ms_unique;
    avg_csv_set12 = avg_csv_set12 + IQA_Set12_Images{i}.csv;
    avg_summer_set12 = avg_summer_set12 + IQA_Set12_Images{i}.summer;
end
avg_psnr_set12 = avg_psnr_set12 / length(IQA_Set12_Images);
avg_ssim_set12 = avg_ssim_set12 / length(IQA_Set12_Images);
avg_cw_ssim_set12 = avg_cw_ssim_set12 / length(IQA_Set12_Images);
avg_unique_set12 = avg_unique_set12 / length(IQA_Set12_Images);
avg_msunique_set12 = avg_msunique_set12 / length(IQA_Set12_Images);
avg_csv_set12 = avg_csv_set12 / length(IQA_Set12_Images);
avg_summer_set12 = avg_summer_set12 / length(IQA_Set12_Images);

