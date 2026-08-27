#include <bits/stdc++.h>
using namespace std;
#define rep(i, n) for (int i = 0; i < n; i++)
const int N = 2e5 + 7;
int A[N], X[N];

void solve() {
    int n, m, a, i, j;
    cin >> n >> m;
    rep(i, n) {
        cin >> a;
        A[a - 1] = i;
        X[i] = a - 1;
    }

    // count inversions
    auto ci = [&](int i) -> int {
        if (i < 0 || i == n - 1) return 0;
        return A[i] >= A[i + 1];
    };

    int ans = 1;
    rep(i, n - 1) ans += ci(i);

    rep(_, m) {
        cin >> i >> j;
        i--; j--;
        set<int> affected = {X[i] - 1, X[i], X[j] - 1, X[j]};
        for (auto& i : affected) ans -= ci(i);
        swap(X[i], X[j]);
        swap(A[X[i]], A[X[j]]);
        for (auto& i : affected) ans += ci(i);
        cout << ans << endl;
    }
}


int main() {
    ios::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);
    solve();
}
