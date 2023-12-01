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
    if is_rgb
        x = rgb2lab(x);
    else
        x = cat(3, x, x, x);
    end

    y = x;

    block_size = 32;
    image_shape = size(x);
    x_remainder = mod(image_shape(1), block_size);
    y_remainder = mod(image_shape(2), block_size);
    num_xblocks = floor(image_shape(1) / block_size);
    num_yblocks = floor(image_shape(2) / block_size);

    for i = 0:(num_xblocks-1)
        for j = 0:(num_yblocks-1)
            y_offset = (i * block_size + 1);
            x_offset = (j * block_size + 1);
            block = imcrop(x, [x_offset, y_offset, block_size-1, block_size-1]);
            block_dist = sqrt(sum(block.^2, 3));
            block_sigma = sqrt(var(block_dist(:)));
            block = imnlmfilt(block, 'DegreeOfSmoothing', 1.1 * block_sigma + 0.001, 'SearchWindowSize', 21, 'ComparisonWindowSize', 5);
            % block = imnlmfilt(block);
            y(y_offset:(y_offset+block_size-1), x_offset:(x_offset+block_size-1),:) = block;
            % imshow(lab2rgb(block));
        end
    end

    % y_remainder_start = num_yblocks*block_size+1;
    % y_remainder_stop = image_shape(1);
    % x_remainder_start = num_xblocks*block_size+1;
    % x_remainder_stop = image_shape(2);
    % y(y_remainder_start:y_remainder_stop, :, :) = x(y_remainder_start:y_remainder_stop, :, :);
    % y(x_remainder_start:x_remainder_stop, :, :) = x(x_remainder_start:x_remainder_stop, :, :);

    x = y;

    % RUN NLM FILTER
    % x = imnlmfilt(x, 'DegreeOfSmoothing', 10, 'SearchWindowSize', 9);
    % x = imnlmfilt(x, 'SearchWindowSize', 5);
    % x = imnlmfilt(x);

    % CONVERT BACK TO RGB IF PROVIDED IN RGB
    if is_rgb
        x = lab2rgb(x);
    else
        x = x(:, :, 1);
    end

    % SAVE IMAGE OUT
    if image_out.contains(".MAT")
        save(image_out, "x")
    else
        imwrite(x, image_out);
    end
end

