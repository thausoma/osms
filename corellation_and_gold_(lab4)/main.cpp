#include <iostream>
using namespace std;

const int REGISTER_LENGTH = 5;
const int SEQUENCE_LENGTH = 31;

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
        int outX = clockRegister(x, 3, 4);
        int outY = clockRegister(y, 1, 4);
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

    printTable(gold, gold, "Автокорреляция исходной последовательности");
    cout << endl;

    cout << "Взаимная корреляция (сдвиг 0): " << correlation(gold, goldNew, 0) << endl;
    cout << endl;

    printTable(gold, goldNew, "Взаимная корреляция исходной и новой по сдвигам");

    return 0;
}