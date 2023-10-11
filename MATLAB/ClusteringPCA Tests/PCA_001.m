clear
close all;
clc;

%%%%%%%%%%%%%% Final Project - Part 3 %%%%%%%%%%%%%%%%%%%

%Image Training%

%Training Image Readings
TrainingFiles = dir('Training\*.jpg');
training_count = length(TrainingFiles);
train_imgs = cell(1, training_count);

%Average Face Vector
for k = 1:training_count
        train_file = fullfile('Training\', TrainingFiles(k).name);
        train_imgs{k} = imread(train_file);
        train_imgs2{k} = rgb2gray(train_imgs{k});
        % [row, column] = size(train_imgs{k});
        % pixel_count = row*column;
        double_img = double(train_imgs2{k});
        % [row, column] = size(double_img);
        
        Y(:,k) = reshape(double_img(1:70,1:70), 70*70, 1);
end

avgvect = mean(Y,2);

for k = 1:training_count
    Y(:,k) = Y(:,k) - avgvect;
end

%Eigenvalues/vectors
C = Y.'*Y;
[eigvects, eigvals] = eig(C);
eigvals = eigvals*ones(training_count,1);
eigen = [eigvals eigvects.'];
eigen = sortrows(eigen,'descend');

eigvals = eigen(:,1);
eigvects(:,:) = eigen(:,2:training_count+1);

%PCA training
thr = 0.98;
m = 1;
eigval_total = sum(eigvals);
val = eigvals(1,1)/eigval_total;
while val <= thr
    m = m+1;
    val = sum(eigvals(1:m,1))/eigval_total;
end

u(:,1:m) = Y*eigvects(:,1:m);
u = u/norm(u);

%Training Weight Matrix
for k = 1:training_count
    for j = 1:m
        w(j,k) = u(:,j).'*Y(:,k);
    end
end

%Image Testing%

%Testing Image Readings
TestingFiles = dir('Testing\*.jpg');
testing_count = length(TestingFiles);
test_imgs = cell(1, testing_count);

for k = 1:testing_count
        test_file = fullfile('Testing\', TestingFiles(k).name);
        test_imgs{k} = imread(test_file);
        test_imgs2{k} = rgb2gray(test_imgs{k});
        % [row, column] = size(test_imgs{k});
        % pixel_count = row*column;
        double_img = double(test_imgs2{k});
        
        X(:,k) = reshape(double_img(1:70,1:70), 70*70, 1)-avgvect;
end

%Testing Weight Matrix
for k = 1:testing_count
    for j = 1:m
        w_test(j,k) = u(:,j).'*X(:,k);
    end
end

%Euclidean Distance Calculation
for k = 1:testing_count
    for j = 1:training_count
        Euc(j,k) = sqrt(sum((w_test(:,k)-w(:,j)).^2));
    end
end

%Face Matching
for k = 1:testing_count
    [distance, idx] = min(Euc(:,k));
    %pair = [test_imgs{k}, train_imgs{idx}];
    figure(k);
    subplot(2,1,1), imshow(test_imgs{k})
    subplot(2,1,2), imshow(train_imgs{idx})
    %imshow(pair);
end