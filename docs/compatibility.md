# Compatibility & acceptance checks

## v2rayNG

Format: JSON array of complete Xray profiles (`sub/v2rayng.json`). Verify in the target app version:

1. Import URL from subscription settings on Android.
2. Update and confirm **exactly 7** profiles with unique names.
3. Test each profile's runtime startup and real connectivity separately on the target network. A successful import does not imply working connectivity.
4. Run subscription update again; confirm there are still **exactly 7** profiles and that edits replace originals rather than duplicating them.
5. On a subsequent test commit, change one harmless display field and verify update propagation, then revert.
6. Check for core errors, DNS failures, route conflicts, and unintended traffic leaks.

Known upstream reports: [v2rayNG array-update duplication](https://github.com/2dust/v2rayNG/issues/5421) and [fractional numeric conversion](https://github.com/2dust/v2rayNG/issues/6291). Applicability depends on app version and should be verified on device.

## Hiddify

Native Xray full JSON is not equivalent to sing-box JSON or a share-link subscription. Current output deliberately unsupported. Hiddify future format requires a separately implemented and tested configuration; do not label converted direct outbounds as VPN proxy servers.

## Public-release checklist

- [ ] Confirm SOCKS endpoint ownership and permission to disclose its IP.
- [ ] Test Xray core version and all referenced geosite/geoip assets.
- [ ] Test the four altered DNS outbound references on real networks.
- [ ] Confirm `127.0.0.1:10853` does not conflict with client-managed DNS.
- [ ] Test carrier-specific profiles on corresponding networks.
- [ ] Confirm first and second subscription refresh in the chosen v2rayNG version.
- [ ] Confirm GitHub Raw reachability where intended; prepare mirror if necessary.
- [ ] Keep source changes and generated subscription in the same commit.
