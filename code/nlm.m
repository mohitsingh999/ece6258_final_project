function nlm(image_in, image_out, is_rgb)
    % MAKE SURE THESE ARE STRINGS
    image_in = string(image_in);
    image_out = string(image_out);
    % LOAD IMAGE IN
    if image_in.contains(".MAT")
        load(image_in)
    else
        x = imread(image_in);
    end

    % % CONVERT TO CIE IF IN RGB
    % if is_rgb
    %     x = rgb2lab(x);
    % end

    % RUN NLM FILTER
    % y_cie = imnlmfilt(x_cie, 'DegreeOfSmoothing', 0.0001);
    % y = imnlmfilt(x, 'SearchWindowSize', 5);
    y = imnlmfilt(x);

    % % CONVERT BACK TO RGB IF PROVIDED IN RGB
    % if is_rgb
    %     y = lab2rgb(y_cie);
    % end

    % SAVE IMAGE OUT
    if image_out.contains(".MAT")
        save(image_out, "y")
    else
        imwrite(y, image_out);
    end
end

