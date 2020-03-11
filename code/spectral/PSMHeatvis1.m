% 2D heat EQ visualization
clear
fsize = 12; %font size
cd('/home/elsaida/spectral') %kataloog kus on datafail
load('heat_eq_test_12_04.mat'); % failinimi
U02D=reshape(u0,[punktide_arv,punktide_arv]); % initial condition

for i=1:length(tv)
 Lah2D{i,1}=reshape(lahend(i,:),[punktide_arv,punktide_arv]);
end

% plotting
for i=1:length(tv)
 hh=figure(i)
 contour(Lah2D{i,1})
 l1=legend(['T = ',num2str(tv(i),'% 10.2f')],'Location','SouthWest');
 set(l1,'FontName','Times','FontSize',fsize);
 set(gca,'FontName','Times','FontSize',fsize); %axis to correct font
 grid on; pbaspect([1 1 1]); %grid and aspect ratio
 print(hh,sprintf('%d_T_%d.eps',i,tv(i)),'-dpsc2'); %plot eps
end