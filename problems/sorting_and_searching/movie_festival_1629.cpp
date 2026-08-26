#include <bits/stdc++.h>
using namespace std;

#define rep(i, n) for (int i = 0; i < n; i++)

/*
    classic scheduling max non overlaps
    greedy works
*/

void solve() {
    int n, a, b;
    cin >> n;
    vector<pair<int, int>> vec(n);
    rep(i, n) {
        cin >> a >> b;
        vec[i] = make_pair(b, a);
    }
    sort(vec.begin(), vec.end());


    int ans = 0;
    int t = 0;
    for (auto& [b, a] : vec) {
        if (a < t) continue;
        ans++;
        t = b;
    }

    cout << ans << endl;
}


int main() {
    ios::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);

    int t = 1;
    // cin >> t;
    while (t--) solve();
}
