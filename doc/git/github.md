# Git issues
#### pull/push timeout/connection reset: https://zhuanlan.zhihu.com/p/636418854
Using Clash:
- git config --global http.proxy http://127.0.0.1:7890 
- git config --global https.proxy http://127.0.0.1:7890

Remove proxy:
- git config --global --unset http.proxy
- git config --global --unset https.proxy

Review Proxy:
- git config --global --get http.proxy
- git config --global --get https.proxy
