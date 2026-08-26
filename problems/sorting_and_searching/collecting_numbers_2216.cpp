#include <bits/stdc++.h>
using namespace std;
#define rep(i, n) for (int i = 0; i < n; i++)
const int N = 2e5 + 7;
int A[N];

void solve() {
    int n, a;
    cin >> n;
    rep(i, n) {
        cin >> a;
        A[a - 1] = i;
    }

    int ans = 1;
    rep(i, n - 1) {
        if (A[i] < A[i + 1]) continue;
        ans++;
    }

    cout << ans << endl;
}


int main() {
    ios::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);
    solve();
}
