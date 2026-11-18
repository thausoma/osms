clear; clc;

P   = 31;
REG = 5;
journalNumber = 24;

gold = makeGold(journalNumber,journalNumber + 7);
goldNew = makeGold(journalNumber + 1, journalNumber + 7 - 5);

disp('Исходная последовательность Голда:');  disp(gold);
disp('Новая последовательность (x+1, y-5):'); disp(goldNew);

g = 2*gold - 1;
gNew = 2*goldNew - 1;

[Rraw, lags] = xcorr([g g], g, P-1);
Rauto = Rraw(lags >= 0) / P;

fprintf('Сдвиг | Автокорреляция\n');
for k = 0:P-1
    fprintf('%5d | % .4f\n', k, Rauto(k+1));
end

[Rcraw, clags] = xcorr([gNew gNew], g, P-1);
Rcross = Rcraw(clags >= 0) / P;
fprintf('Взаимная корреляция (сдвиг 0): % .4f\n', Rcross(1));

Rbuiltin = autocorr(g, 'NumLags', P-1);
fprintf('autocorr: R(0) = % .4f, R(1) = % .4f\n', Rbuiltin(1), Rbuiltin(2));

figure;
stem(0:P-1, Rauto, 'filled');
xlabel('Задержка (lag), отсчётов'); ylabel('R(\tau)');
title('Автокорреляция последовательности Голда (циклическая, xcorr)');
grid on;

function seq = makeGold(x0, y0)
    REG = 5; P = 31;
    x = zeros(1, REG);  y = zeros(1, REG);
    v = x0;
    for i = REG:-1:1
        x(i) = mod(v, 2);  v = floor(v/2);
    end
    v = y0;
    for i = REG:-1:1
        y(i) = mod(v, 2);  v = floor(v/2);
    end
    seq = zeros(1, P);
    for t = 1:P
        outX = x(5);  outY = y(5);
        seq(t) = xor(outX, outY);
        fbX = xor(x(4), x(5));
        fbY = xor(y(2), y(5));
        x = [fbX, x(1:4)];
        y = [fbY, y(1:4)];
    end
end