#include <bits/stdc++.h>
using namespace std;

#define rep(i, n) for (int i = 0; i < n; i++)


void solve() {
	int n, m, k;
	cin >> n >> m >> k;
    vector<int> A(n), B(m);
    rep(i, n) cin >> A[i];
    rep(i, m) cin >> B[i];

    sort(A.begin(), A.end());
    sort(B.begin(), B.end());

    int ans = 0, j = 0, i = 0;
    while (i < n && j < m) {
        if (abs(A[i] - B[j]) <= k) {
            ans++; i++; j++;
            continue;
        }
        if (A[i] < B[j]) i++;
        else j++;
    }

    cout << ans << endl;
}


int main() {
	ios::sync_with_stdio(0);
	cin.tie(0); cout.tie(0);
    solve();
}
