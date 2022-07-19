function parallel_dipha_input( input_dir, valid_filename )
    
    fileID = fopen(valid_filename,'r');
    
    A = fscanf(fileID, '%d');
    
    B = A';
    B = B(:)';
    
    %disp(B);
    parpool(4);
    
    parfor n = 1 : length(B)
        dir = input_dir + string(B(n)) + '/images/';
        disp(dir);
        output = input_dir + string(B(n)) + '/dipha.input';
        save_3d_image_data(dir, output);
    end
    