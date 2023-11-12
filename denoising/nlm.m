function nlm(image_in, image_out)
    x = imread(image_in);
    x_cie = rgb2lab(x);
    % y_cie = imnlmfilt(x_cie, 'DegreeOfSmoothing', 0.0001);
    y_cie = imnlmfilt(x_cie, 'SearchWindowSize', 5);
    y = lab2rgb(y_cie);
    % figure();
    % imshow(x);
    % figure();
    % imshow(y);
    imwrite(y, image_out);
end

