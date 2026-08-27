#include <bits/stdc++.h>
using namespace std;

#define rep(i, n) for (int i = 0; i < n; i++)

// Anti-hack hash: runtime seed prevents adversarial collision attacks on unordered_map
struct custom_hash {
    static uint64_t splitmix64(uint64_t x) {
        x += 0x9e3779b97f4a7c15;
        x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9;
        x = (x ^ (x >> 27)) * 0x94d049bb133111eb;
        return x ^ (x >> 31);
    }

    size_t operator()(uint64_t x) const {
        static const uint64_t FIXED_RANDOM = chrono::steady_clock::now().time_since_epoch().count();
        return splitmix64(x + FIXED_RANDOM);
    }
};

void solve() {
    int n;
    cin >> n;
    vector<int> A(n);
    rep(i, n) cin >> A[i];

    unordered_map<int, int, custom_hash> M;
    int ans = 0, curr = 0, j = 0;
    rep(i, n) {
        M[A[i]]++;
        if (M[A[i]] == 1) {
            curr++;
            ans = max(ans, curr);
            continue;
        }
        while (1) {
            M[A[j]]--; curr--;
            if (M[A[j++]]) break;
        }
        curr++;
    }
    cout << ans << endl;
}


int main() {
    ios::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);
    solve();
}
