#include <bits/stdc++.h>
using namespace std;
#define rep(i, n) for (int i = 0; i < n; i++)


void solve() {
    int n;
    cin >> n;
    vector<int> Q(n);
    rep(i, n) Q[i] = i + 1;

    bool t = true;
    while (Q.size() > 1) {
        vector<int> R;
        for (auto &x : Q) {
            if (t) R.emplace_back(x);
            else cout << x << " ";
            t = !t;
        }
        Q = R;
    }
    cout << Q[0] << endl;
}


int main() {
    ios::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);

    int t = 1;
    // cin >> t;
    while (t--) solve();
}
