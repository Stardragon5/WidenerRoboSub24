clear
close all;
clc

%%%%%%%%%%%%%%%%%%%% VERSION 2 %%%%%%%%%%%%%%%%%%%%

%Variables
R_Total = zeros(1,256);
G_Total = zeros(1,256);
B_Total = zeros(1,256);
temp = zeros(1,1);

for i = 1:5
    %Variables
    str = strcat('Orange',int2str(i),'.jpg');
    Orange = imread(str);
    R = Orange(:,:,1);
    G = Orange(:,:,2);
    B = Orange(:,:,3);
    line = [0 0.1];

    %Mean & Standard Deviation
    r_mean = mean(mean(R));
    g_mean = mean(mean(G));
    b_mean = mean(mean(B));
    r_sd = std2(R);
    g_sd = std2(G);
    b_sd = std2(B);

    %RGB High & Low Values
    %(based on 2 SD)
    r_high = r_mean + 2*r_sd;
    r_low = r_mean - 2*r_sd;
    g_high = g_mean + 2*g_sd;
    g_low = g_mean - 2*g_sd;
    b_high = b_mean + 2*b_sd;
    b_low = b_mean - 2*b_sd;

    %RGB Plot
    figure(i);
    hold on;
    r = histogram(R,0:1:256,'FaceColor','r','Normalization','probability');
    g = histogram(G,0:1:256,'FaceColor','g','Normalization','probability');
    b = histogram(B,0:1:256,'FaceColor','b','Normalization','probability');
    plot(r_low*ones(2,1),line,'color','k','linewidth',2); % r_low line 
    plot(r_high*ones(2,1),line,'color','k','linewidth',2); % r_high line
    plot(g_low*ones(2,1),line,'color','k','linewidth',2); % g_low line 
    plot(g_high*ones(2,1),line,'color','k','linewidth',2); % g_high line
    plot(b_low*ones(2,1),line,'color','k','linewidth',2); % b_low line 
    plot(b_high*ones(2,1),line,'color','k','linewidth',2); % b_high line
    legend('r','g','b');
    
    %Totalling    
    R_Total = [R_Total R(:)'];
    G_Total = [G_Total G(:)'];
    B_Total = [B_Total B(:)'];
end

%Total Mean & SD
r_mean = mean(R_Total);
g_mean = mean(G_Total);
b_mean = mean(B_Total);
r_sd = std2(R_Total);
g_sd = std2(G_Total);
b_sd = std2(B_Total);

%RGB High & Low Values
%(based on 2 SD)
r_high = r_mean + 2*r_sd;
r_low = r_mean - 2*r_sd;
g_high = g_mean + 2*g_sd;
g_low = g_mean - 2*g_sd;
b_high = b_mean + 2*b_sd;
b_low = b_mean - 2*b_sd;

figure(i+1);
hold on;
histogram(R_Total,0:1:256,'FaceColor','r','Normalization','probability');
histogram(G_Total,0:1:256,'FaceColor','g','Normalization','probability');
histogram(B_Total,0:1:256,'FaceColor','b','Normalization','probability');
plot(r_low*ones(2,1),line,'color','k','linewidth',2); % r_low line 
plot(r_high*ones(2,1),line,'color','k','linewidth',2); % r_high line
plot(g_low*ones(2,1),line,'color','k','linewidth',2); % g_low line 
plot(g_high*ones(2,1),line,'color','k','linewidth',2); % g_high line
plot(b_low*ones(2,1),line,'color','k','linewidth',2); % b_low line 
plot(b_high*ones(2,1),line,'color','k','linewidth',2); % b_high line
title('Red RGB Histogram');
xlabel('RGB Value');
ylabel('Frequency (Normalized)');
legend('r','g','b');