#include <cmath>
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;


int main() {
    int n, t, k, a;
    int not_found = -1;
    cin >> t;
    for (int j = 0; j < t; j++) {
        cin >> n;
        bool used[n] = {false};
        not_found = -1;
        for (int i = 0; i < n; i++) {
            cin >> k;
            bool flag = true;
            for (int l = 0; l < k; l++) {
                cin >> a;
                if (!used[a - 1] and flag) {
                    flag = false;
                    used[a - 1] = true;
                }
            }
            if (flag and not_found == -1) {
                not_found = i + 1;
            }
        }
        if (not_found == -1) {
            cout << "OPTIMAL\n";
            continue;
        }
        for (int i = 0; i < n; i++) {
            if (used[i] == false) {
                cout << "IMPROVE\n" << not_found << " " << i+1 << "\n";
                break;
            }
        }
    }
    return 0;
}
