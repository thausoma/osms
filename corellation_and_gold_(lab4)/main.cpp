#include <iostream>
#include <cmath>
using namespace std;

const int REGISTER_LENGTH = 5;
const int SEQUENCE_LENGTH = 31;

const int TAP_X_A = 1, TAP_X_B = 4;
const int TAP_Y_A = 1, TAP_Y_B = 4;

void checkBalance(const int seq[SEQUENCE_LENGTH]) {
    int ones = 0;
    for (int i = 0; i < SEQUENCE_LENGTH; i++) ones += seq[i];
    int zeros = SEQUENCE_LENGTH - ones;
    int expect = 1 << (REGISTER_LENGTH - 1);
    bool ok = abs(ones - zeros) <= 1;
    cout << "Сбалансированность: " << ones << " ед. / " << zeros << " нулей, ожидалось "
         << expect << "/" << expect - 1 << " -> "
         << (ok ? "выполнено" : "нарушено") << endl;
}

void checkRunProperty(const int seq[SEQUENCE_LENGTH]) {
    int counts[SEQUENCE_LENGTH + 1] = {0};
    int total = 0, current = 1;
    for (int i = 1; i < SEQUENCE_LENGTH; i++) {
        if (seq[i] == seq[i - 1]) current++;
        else { counts[current]++; total++; current = 1; }
    }
    counts[current]++; total++;

    double share1 = 100.0 * counts[1] / total;
    cout << "Цикличность: циклы по длинам:";
    for (int len = 1; len <= SEQUENCE_LENGTH; len++)
        if (counts[len]) cout << " " << len << "->" << counts[len];
    cout << "; доля циклов длиной 1: " << share1 << "% (ожидалось ~50%) -> "
         << (fabs(share1 - 50.0) < 10.0 ? "выполнено" : "нарушено") << endl;
}

void checkCorrelationProperty(const int seq[SEQUENCE_LENGTH]) {
    double R0 = 0, max_side = 0;
    int max_shift = 0;
    for (int shift = 0; shift < SEQUENCE_LENGTH; shift++) {
        int matches = 0;
        for (int i = 0; i < SEQUENCE_LENGTH; i++)
            if (seq[i] == seq[(i + shift) % SEQUENCE_LENGTH]) matches++;
        double R = (2.0 * matches - SEQUENCE_LENGTH) / SEQUENCE_LENGTH;
        if (shift == 0) R0 = R;
        else if (fabs(R) > fabs(max_side)) { max_side = R; max_shift = shift; }
    }
    double ideal = -1.0 / SEQUENCE_LENGTH;
    cout << "Корреляция: R(0) = " << R0 << ", макс. боковой лепесток R(" << max_shift
         << ") = " << max_side << " (идеал " << ideal << ") -> "
         << (fabs(R0 - 1.0) < 1e-9 ? "пик в норме" : "пик нарушен")
         << (fabs(max_side - ideal) < 0.1 ? ", боковые возвышения нормальные"
                                          : ", боковые возвышения отклоняются")
         << endl;
}

void checkAllProperties(const int seq[SEQUENCE_LENGTH]) {
    cout << "\nпроверка свойств" << endl;
    checkBalance(seq);
    checkRunProperty(seq);
    checkCorrelationProperty(seq);
}

void decimalToBits(int value, int bits[REGISTER_LENGTH]) {
    for (int i = REGISTER_LENGTH - 1; i >= 0; i--) {
        bits[i] = value % 2;
        value = value / 2;
    }
}

int clockRegister(int reg[REGISTER_LENGTH], int tapA, int tapB) {
    int outputBit = reg[4];
    int feedbackBit = reg[tapA] ^ reg[tapB];
    for (int i = REGISTER_LENGTH - 1; i >= 1; i--) {
        reg[i] = reg[i - 1];
    }
    reg[0] = feedbackBit;
    return outputBit;
}

void makeGoldSequence(int xNumber, int yNumber, int gold[SEQUENCE_LENGTH]) {
    int x[REGISTER_LENGTH];
    int y[REGISTER_LENGTH];
    decimalToBits(xNumber, x);
    decimalToBits(yNumber, y);

    for (int t = 0; t < SEQUENCE_LENGTH; t++) {  
        int outX = clockRegister(x, TAP_X_A, TAP_X_B);
        int outY = clockRegister(y, TAP_Y_A, TAP_Y_B);
        gold[t] = outX ^ outY;
    }
}

double correlation(const int a[SEQUENCE_LENGTH], const int b[SEQUENCE_LENGTH], int shift) {
    int matches = 0;
    int mismatches = 0;
    for (int i = 0; i < SEQUENCE_LENGTH; i++) {
        if (a[i] == b[(i + shift) % SEQUENCE_LENGTH]) {
            matches++;
        } else {
            mismatches++;
        }
    }
    return (matches - mismatches) / 31.0;
}

void printBits(const int seq[SEQUENCE_LENGTH], int shift) {
    for (int i = 0; i < SEQUENCE_LENGTH; i++) {
        cout << seq[(i + shift) % SEQUENCE_LENGTH];
    }
}

void printTable(const int a[SEQUENCE_LENGTH], const int b[SEQUENCE_LENGTH], const char* title) {
    cout << title << endl;
    cout << "Сдвиг | Исходная                        | Сдвинутая                       | Корреляция" << endl;
    for (int shift = 0; shift < SEQUENCE_LENGTH; shift++) {
        cout << shift << " | ";
        printBits(a, 0);
        cout << " | ";
        printBits(b, shift);
        cout << " | " << correlation(a, b, shift) << endl;
    }
}

void printSequence(const char* name, const int seq[SEQUENCE_LENGTH]) {
    cout << name << ": ";
    for (int i = 0; i < SEQUENCE_LENGTH; i++) {
        cout << seq[i] << ' ';
    }
    cout << endl;
}

int main() {
    const int journalNumber = 24;
    int gold[SEQUENCE_LENGTH];
    int goldNew[SEQUENCE_LENGTH];
    makeGoldSequence(journalNumber, journalNumber + 7, gold);
    makeGoldSequence(journalNumber + 1, journalNumber + 7 - 5, goldNew);
    printSequence("Исходная последовательность Голда", gold);
    printSequence("Новая последовательность Голда (x+1, y-5)", goldNew);
    cout << endl;

    checkAllProperties(gold);
    
    cout << "\n\n";
    printTable(gold, gold, "Автокорреляция исходной последовательности");
    cout << endl;
    cout << "Взаимная корреляция (сдвиг 0): " << correlation(gold, goldNew, 0) << endl;
    cout << endl;
    printTable(gold, goldNew, "Взаимная корреляция исходной и новой по сдвигам");
    return 0;
}