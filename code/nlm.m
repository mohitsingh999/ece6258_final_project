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

    % CONVERT TO CIE IF IN RGB
    % if is_rgb
    %     x = rgb2lab(x);
    % end

    % RUN NLM FILTER
    % x = imnlmfilt(x, 'DegreeOfSmoothing', 0.0001);
    % x = imnlmfilt(x, 'SearchWindowSize', 5);
    x = imnlmfilt(x);

    % CONVERT BACK TO RGB IF PROVIDED IN RGB
    % if is_rgb
    %     x = lab2rgb(x);
    % end

    % SAVE IMAGE OUT
    if image_out.contains(".MAT")
        save(image_out, "x")
    else
        imwrite(x, image_out);
    end
end

