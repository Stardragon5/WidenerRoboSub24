clear
close all;
clc;

%%%%%%%%%%%%%% Final Project - Part 2 %%%%%%%%%%%%%%%%%%%

%Variables
A = imread('24Capture.jpg');
B = rgb2gray(A);
[length, width, depth] = size(A);

%Image Plotting
figure(1);
imshow(A);

figure(2);
imshow(B);

%Variable Editing - Column Features
r_temp = double(A(:,:,1));
g_temp = double(A(:,:,2));
b_temp = double(A(:,:,3));
[r] = double(r_temp(:));
[g] = double(g_temp(:));
[b] = double(b_temp(:));
[imrow] = double(B(:));

xy = zeros(length*width, 2);
y = 1:length; 
x = 1:width; 
a = 1;
for i=1:width     
    for j=length:-1:1         
        xy(a,1:2)=[x(i),y(j)];   
        a = a+1;
    end
end

Am = [xy, r, g, b]; 
Bm = [xy, imrow];  

%k-means Algorithm for B
for i = 3:5
    [idx,C,sumd] = kmeans(Bm(:,3),i);  
  
    figure(i); 
    hold on; 
    plot(Bm(idx==1,1),Bm(idx==1,2),'r.','MarkerSize',12);
    plot(Bm(idx==2,1),Bm(idx==2,2),'b.','MarkerSize',12); 
    plot(Bm(idx==3,1),Bm(idx==3,2),'k.','MarkerSize',12);
    if(i==3)
        legend('Cluster 1', 'Cluster 2', 'Cluster 3', 'Location', 'NW'); 
    elseif(i==4)
        plot(Bm(idx==4,1),Bm(idx==4,2),'g.','MarkerSize',12);
        legend('Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4', 'Location', 'NW'); 
    else
        plot(Bm(idx==4,1),Bm(idx==4,2),'g.','MarkerSize',12);
        plot(Bm(idx==5,1),Bm(idx==5,2),'c.','MarkerSize',12);
        legend('Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4', 'Cluster 5', 'Location', 'NW');
    end
    title('Cluster Assignments'); 
    hold off; 
end

%k-means Algorithm for A
for i = 4:5
    [idx,C,sumd] = kmeans(Am(:,3),i);  
  
    figure(2+i); 
    hold on; 
    plot(Am(idx==1,1),Am(idx==1,2),'r.','MarkerSize',12);
    plot(Am(idx==2,1),Am(idx==2,2),'b.','MarkerSize',12); 
    plot(Am(idx==3,1),Am(idx==3,2),'k.','MarkerSize',12);
    plot(Am(idx==4,1),Am(idx==4,2),'g.','MarkerSize',12);
    if(i==4)
        legend('Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4', 'Location', 'NW'); 
    else
        plot(Am(idx==5,1),Am(idx==5,2),'c.','MarkerSize',12);
        legend('Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4', 'Cluster 5', 'Location', 'NW');
    end
    title('Cluster Assignments'); 
    hold off; 
end