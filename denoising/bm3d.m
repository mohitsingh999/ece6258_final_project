function bm3d(image_in, image_out)
    addpath("./BM3D/")
    im = rgb2gray(imread(image_in));
    sigma = 5;
    [NA, im_bm3d] = BM3D(1, im, sigma);
    save(image_out, "im_bm3d");
end
