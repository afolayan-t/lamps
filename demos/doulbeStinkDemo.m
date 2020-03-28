%%%%

nPoints = 500;
len = 25;

y = linspace(0-len,0+len, nPoints);
x = linspace(0-len,0+len, nPoints);

[XS, YS] = meshgrid(x,y);
% perception = strength*e^(-(1/radius)*r) r = distance from origin

%%% SET PARAMETERS
nosePosition = [0,0];
noseRadius = 6;
noseStrength = 1;

%%% STINKY FOOD 1
stinkRadius = 4;
stinkStrength = 1.5;
stinkPosition = [7,-6];
stink = stinkStrength*exp(-(1/stinkRadius)*...
    ((XS-stinkPosition(1)).^2+(YS- stinkPosition(2)).^2).^(1/2));

stink2Radius = 3;
stink2Strength = 2;
stink2Position = [-7,7];
stink2 = stink2Strength*exp(-(1/stink2Radius)*...
    ((XS-stink2Position(1)).^2+(YS- stink2Position(2)).^2).^(1/2));


detectionThreshold = noseStrength*stinkStrength*exp(-2);

% r = ( (x-x0)^2 + (y-y0)^2 ) ^ (1/2)

perceptionWord = 'Lamp';
stinkWord = 'Stinky food';
for i = 1:60
    %%% HAVE NOSE DO RANDOM WALK
    nosePosition = nosePosition + 2*(rand(1, 2) - .5);
    smellPerception = noseStrength*exp(-(1/noseRadius)*...
        ((XS-nosePosition(1)).^2+(YS - nosePosition(2)).^2).^(1/2));
    
    
    %%% SCENT PERCEPTION IS DIRECTION OF MAX DETECTION
    scentPerception = smellPerception.*stink + smellPerception.*stink2;
    
    [maxScentStrength,maxDex] = max(scentPerception(:));
    %%%% POSITION OF MAX DETECTION
    [xDex,yDex] = ind2sub(size(XS),maxDex);
    foodVector = [XS(xDex, yDex) YS(xDex, yDex)] - nosePosition;
    
    foodVector = 10*maxScentStrength*(foodVector./norm(foodVector));
    fprintf('Max Detection: %f\n', maxScentStrength)
    
    cla
    surf(XS,YS,smellPerception,'LineStyle', 'none')
    %%% ADD LABELS ABOVE EACH PEAK
    text(nosePosition(1), nosePosition(2), 1.2*noseStrength, perceptionWord,...
        'FontName', 'monospaced', 'fontsize', 15, ...
        'HorizontalAlignment', 'center');
    text(stinkPosition(1), stinkPosition(2), 1.2*stinkStrength, stinkWord,...
        'FontName', 'monospaced', 'fontsize', 15, ...
        'HorizontalAlignment', 'center');
    text(stink2Position(1), stink2Position(2), 1.2*stink2Strength, stinkWord,...
        'FontName', 'monospaced', 'fontsize', 15, ...
        'HorizontalAlignment', 'center');
    hold on
    %%% STINK 1
    surf(XS, YS, stink, 'LineStyle', 'none', 'FaceColor','interp')
    
    surf(XS, YS, stink2, 'LineStyle', 'none', 'FaceColor','interp')
    if maxScentStrength > detectionThreshold
            %%% POSITION OF MAX DETECTION
    stem3(XS(xDex, yDex), YS(xDex, yDex), stink2Strength,...
        'LineWidth', 5, 'MarkerSize', 15);
    %%% DRAW CONNECTION BETWEEN PEAKS
    quiver3(nosePosition(1), nosePosition(2), noseStrength, ...
        foodVector(1), foodVector(2), 0, 'LineWidth', 5, 'color', 'k',...
        'MarkerEdgeColor', 'k')
    end
    %%% SET GRAPH PROPERTIES 
    ylim([-len len])
    xlim([-len len])
    zlim([0 2])
    xlabel('inches')
    ylabel('planck length')
    zlabel('Stink magnitude')
    set(gca,'FontName', 'monospaced')
    set(gca, 'FontSize', 15)
    pause(.2)
    
    saveas(gcf, sprintf('doubleStinkFrame%0.0d.png', i))
end

