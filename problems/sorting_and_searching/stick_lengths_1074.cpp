#include <bits/stdc++.h>
using namespace std;

#define rep(i, n) for (int i = 0; i < n; i++)


void solve() {
    int n;
    cin >> n;
    vector<int> P(n);
    rep(i, n) cin >> P[i];
    sort(P.begin(), P.end());

    // pick middle stick
    int mid = P[n / 2];

    long long ans = 0;
    rep(i, n) ans += abs(P[i] - mid);
    cout << ans << endl;
}


int main() {
    ios::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);
    solve();
}
