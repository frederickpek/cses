#include <bits/stdc++.h>
using namespace std;
#define rep(i, n) for (int i = 0; i < n; i++)
const int N = 1e3 + 7;
const int X = 1e5 + 7;
int dp[N][X];
int H[N], S[N];

/*
    0/1 knapsack
    dp[i][x] be max pages obtainable with first i books with max budget of x
    dp[0][x] = 0, for all x

    transition
    dp[i][x] >= dp[i - 1][x]                (skip ith book)
    dp[i][x] >= dp[i - 1][x - H[i]] + S[i]  (use ith book)
    dp[i][x] = max(dp[i - 1][x], dp[i - 1][x - H[i]] + S[i])

    ---
    
    for understanding
    claim: dp[i][x] equals max pages obtainable with first i books with max budget of x
    base case: dp[0][x] = 0, no books, no pages

    inductive step:
    assume dp[i - 1][x] is correct for all x. for book i, any valid subset of 1..i either:
    1. doesn't include book i, then the best is dp[i - 1][x] (correct by hypothesis)
    2. includes book i, then we spend H[i] cost and gain S[i] pages, and the remaining books 1..i-1 must fit in budget x - H[i], giving dp[i - 1][x - H[i]] + S[i] (correct by hypothesis)
    
    both cases are mutually exclusive and exhaustive, book i is either in the subset or not, taking max of both gives the true optimum
*/

void solve() {
    int n, x;
    cin >> n >> x;
    rep(i, n) cin >> H[i + 1];
    rep(i, n) cin >> S[i + 1];

    rep(i, n + 1) rep(j, x + 1) {
        if (i == 0) continue;
        dp[i][j] = dp[i - 1][j];
        if (j - H[i] < 0) continue;
        dp[i][j] = max(dp[i][j], dp[i - 1][j - H[i]] + S[i]);
    }

    cout << dp[n][x] << endl;
}


int main() {
    ios::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);

    int t = 1;
    // cin >> t;
    while (t--) solve();
}
