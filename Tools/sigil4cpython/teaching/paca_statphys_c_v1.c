/* SPDX-License-Identifier: MIT
 * PACA NUKLEA C99 teaching CLI. No CPython internals, dynamic I/O or plugins.
 * Usage: paca_statphys_c_v1 +++ 1 0  (spins, J, h)
 */
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int bounded_integer(const char *text, int *out) {
    char *end = NULL;
    long value;
    errno = 0;
    if (text == NULL || *text == '\0') return 0;
    value = strtol(text, &end, 10);
    if (errno != 0 || *end != '\0' || value < -1000 || value > 1000)
        return 0;
    *out = (int)value;
    return 1;
}

int main(int argc, char **argv) {
    int coupling, field;
    long long bonds = 0, magnetization = 0, result;
    size_t i, n;
    if (argc != 4 || !bounded_integer(argv[2], &coupling) ||
        !bounded_integer(argv[3], &field)) {
        fputs("usage: paca_statphys_c_v1 <+/- spins> <J> <h>\n", stderr);
        return 2;
    }
    n = strlen(argv[1]);
    if (n < 3 || n > 12) {
        fputs("requires 3..12 spins\n", stderr);
        return 2;
    }
    for (i = 0; i < n; ++i) {
        int a, b;
        if ((argv[1][i] != '+') && (argv[1][i] != '-')) {
            fputs("only + and - spin labels\n", stderr);
            return 2;
        }
        a = argv[1][i] == '+' ? 1 : -1;
        b = argv[1][(i + 1) % n] == '+' ? 1 : -1;
        if (argv[1][(i + 1) % n] != '+' &&
            argv[1][(i + 1) % n] != '-') {
            fputs("only + and - spin labels\n", stderr);
            return 2;
        }
        bonds += a * b;
        magnetization += a;
    }
    result = -(long long)coupling * bonds - (long long)field * magnetization;
    printf("%lld\n", result);
    return 0;
}
