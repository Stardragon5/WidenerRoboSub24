clear
close all;
clc

%%%%%%%%%%%%%%%%%%%% VERSION 3 %%%%%%%%%%%%%%%%%%%%

%Variables
color = ["Red" "Orange" "Yellow" "Green" "Blue" "Purple" "Black" "Noise"];
mult = 1.3;
fprintf('Results from Analysis with +/- %.2f SD\n',mult);
fprintf('______________________________________________________\n');
fprintf('Color\tR_low\tR_high\tG_low\tG_high\tB_low\tB_high\n');

for i = 1:length(color)
    %Variables
    clear R_Total G_Total B_Total
    R_Total = zeros(1,256);
    G_Total = zeros(1,256);
    B_Total = zeros(1,256);

    for j = 1:5
        %Variables
        chr = convertStringsToChars(color(i));
        str = strcat(chr,int2str(j),'.jpg');
        Data = imread(str);
        R = Data(:,:,1);
        G = Data(:,:,2);
        B = Data(:,:,3);
        line = [0 0.1];

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
    r_high = r_mean + mult*r_sd;
    r_low = r_mean - mult*r_sd;
    g_high = g_mean + mult*g_sd;
    g_low = g_mean - mult*g_sd;
    b_high = b_mean + mult*b_sd;
    b_low = b_mean - mult*b_sd;
    fprintf('%s \t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\n',color(i),r_low,r_high,g_low,g_high,b_low,b_high);

    %Display Results
    
    
    %Plot RGB Histogram
    figure(i);
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
    tit = strcat(color(i),' RGB Histogram');
    title(tit);
    xlabel('RGB Value');
    ylabel('Frequency (Normalized)');
    legend('r','g','b');
    
    %3D Plot Points
    x = [r_low r_high r_high r_low r_low; r_low r_high r_high r_low r_low];
    y = [g_low g_low g_high g_high g_low; g_low g_low g_high g_high g_low];
    z = [b_low*ones(1,size(x,2)); b_high*ones(1,size(x,2))];
    r_trip = r_mean/255;
    g_trip = g_mean/255;
    b_trip = b_mean/255;
    trip = [r_trip g_trip b_trip];
    
    %3D Plot
    figure(length(color)+1);
    Temp = surf(x, y, z, 'FaceColor', trip);
    hold on
    grid on
    patch(x', y', z', trip)
    x1 = xlabel('Red');
    x1.FontSize = 28;
    y1 = ylabel('Green');
    y1.FontSize = 28;
    z1 = zlabel('Blue');
    z1.FontSize = 28;
    axis([-10 265 -10 265 -10 265]);
    view(-25, 30)
    t = title('RGB Value Ranges');
    t.FontSize = 40;
    
    figure(length(color)+2);
    hold on
    grid on
    plot3(R_Total, G_Total, B_Total, '.', 'Color', trip, 'MarkerSize', 2);
    xlabel('Red');
    ylabel('Green');
    zlabel('Blue');
    axis([-10 265 -10 265 -10 265]);
    view(-25, 30)
end