clear
close all;
clc;

%%%%%%%%%%%%%% Final Project - Part 1 %%%%%%%%%%%%%%%%%%%

%Variables
X = rgb2gray(imread('15Capture.jpg'));
Y = rgb2gray(imread('15Capture.jpg'));
order = [3 3; 5 5];

%Image Plotting
figure(1);
imshow(X);

figure(2);
imshow(Y);

%Noise Variance Estimate
noise = Y-X;
noise_var = var(double(noise(:)));

%Image Smoothing
% for i = 1:2
%     %Average Filter
%     avg_mask = fspecial('average', order(i,:));
%     avg_filt = imfilter(Y, avg_mask);
%     avg_PSNR = psnr(avg_filt, X);
%     figure(2+i);
%     imshow(avg_filt);
% 
%     %Gaussian Filter w/ sigma = 1
%     gau_mask_1 = fspecial('gaussian', order(i,:), 1);
%     gau_filt_1 = imfilter(Y, gau_mask_1);
%     gau_PSNR_1 = psnr(gau_filt_1, X);
%     figure(4+i);
%     imshow(gau_filt_1);
% 
%     %Gaussian Filter w/ sigma = 2
%     gau_mask_2 = fspecial('gaussian', order(i,:), 2);
%     gau_filt_2 = imfilter(Y, gau_mask_2);
%     gau_PSNR_2 = psnr(gau_filt_2, X);
%     figure(6+i);
%     imshow(gau_filt_2);
% 
%     %Median Filter
%     med_filt = medfilt2(Y, order(i,:));
%     med_PSNR = psnr(med_filt, X);
%     figure(8+i);
%     imshow(med_filt);
% end

%Fourier Transform
% for i = 1:2
%     if i == 1
%         FT = fft2(X);
%     else
%         FT = fft2(Y);
%     end
%     FT_shift = fftshift(FT);
% 
%     %Conversion for plotting
%     temp1 = abs(FT);
%     temp1 = temp1-min(temp1(:));
%     temp1 = 255*temp1./max(temp1(:));
% 
%     temp2 = abs(FT_shift);
%     temp2 = temp2-min(temp2(:));
%     temp2 = 255*temp2./max(temp2(:));
% 
%     %Plotting magnitude
%     figure(8+3*i);
%     imshow(temp1);
% 
%     figure(9+3*i);
%     imshow(temp2);
% 
%     %Plotting angle
%     FT_ang = atan2(imag(FT), real(FT));
%     figure(10+3*i);
%     imshow(FT_ang);
% end

%Edge Detection
sobel = edge(Y, 'sobel');
[~, th2] = edge(Y, 'log');
log = edge(Y, 'log', 1.7*th2, 2.4);
[~, th3] = edge(Y, 'canny');
canny = edge(Y, 'canny', 1.2*th3, 3.25);

%Plotting edge detection
figure(17);
imshow(sobel);

figure(18);
imshow(log);

figure(19);
imshow(canny);