clear
close all;
clc

%%%%%%%%%%%%%%%%%%%% VERSION 1 %%%%%%%%%%%%%%%%%%%%

%Variables
Orange1 = imread('Orange1.jpg');
line = [0 0.1];

%Mean & Standard Deviation
r_mean = mean(mean(Orange1(:,:,1)));
g_mean = mean(mean(Orange1(:,:,2)));
b_mean = mean(mean(Orange1(:,:,3)));
r_sd = std2(Orange1(:,:,1));
g_sd = std2(Orange1(:,:,2));
b_sd = std2(Orange1(:,:,3));

%RGB High & Low Values
%(based on 2 SD)
r_high = r_mean + 2*r_sd;
r_low = r_mean - 2*r_sd;
g_high = g_mean + 2*g_sd;
g_low = g_mean - 2*g_sd;
b_high = b_mean + 2*b_sd;
b_low = b_mean - 2*b_sd;

%RGB Plot
figure(1);
hold on;
x = histogram(Orange1(:,:,1),'FaceColor','r','Normalization','probability');
histogram(Orange1(:,:,2),'FaceColor','g','Normalization','probability');
histogram(Orange1(:,:,3),'FaceColor','b','Normalization','probability');
plot(r_low*ones(2,1),line,'color','k','linewidth',2); % r_low line 
plot(r_high*ones(2,1),line,'color','k','linewidth',2); % r_high line
plot(g_low*ones(2,1),line,'color','k','linewidth',2); % g_low line 
plot(g_high*ones(2,1),line,'color','k','linewidth',2); % g_high line
plot(b_low*ones(2,1),line,'color','k','linewidth',2); % b_low line 
plot(b_high*ones(2,1),line,'color','k','linewidth',2); % b_high line
legend('r','g','b');