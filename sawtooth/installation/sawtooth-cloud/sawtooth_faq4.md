# Sawtooth Permissioning

### How to solve this error ``Wait timed out! Policy was not committed... PENDING`` when ``sawtooth identity policy create`` is run?
--------------------------------------
* There is a possibility that rest-api is down or identity-tp is not running or it might be due to permissioning issues.
* If the cause is due to permissioning, follow these steps:

    - ``sawset proposal create --key /etc/sawtooth/keys/validator.priv sawtooth.identity.allowed_keys={user pub key created through 'sawtooth keygen'}``  
    - ``sawtooth identity policy create policy_1 "PERMIT_KEY {key1}" "PERMIT_KEY {key2}"``  
    - ``sawtooth identity role create transactor policy_1``  

* Refer https://sawtooth.hyperledger.org/docs/core/nightly/master/sysadmin_guide/configuring_permissions.html for detailed information.  


# Appendix: Sawtooth Videos

### Selected YouTube Videos

### 2018 YouTube Videos
* Hyperledger Sawtooth Seafood Supply Chain Demo (3:21, Bitwise, 2018)
    https://www.youtube.com/watch?v=q0T8qAyzY30
* Intel: Building Blockchain for the Enterprise. Shows how Sawtooth builds are done on AWS (5:33, Ryan Beck-Buysse, Bitwise, Lana Kalashnyk, AWS, 2018)
    https://www.youtube.com/watch?v=B_L_PjlSywA
* Sawtooth 1.0 Architecture and App Development (31:26, Zac Delventhal, Bitwise, 2018)
    https://www.youtube.com/watch?v=uBebFQM49Xk
* Blockchain and Hyperledger Sawtooth Overview (6:15, Daniel Homlund Martin Kronberg and Daniel Homlund, Intel, 2018)
    https://www.youtube.com/watch?v=HwFItjV6Czo
* Several Sawtooth application development tutorials by John S.
    https://www.youtube.com/channel/UC4YOKxLGKFcaq4duRhH75qw

* Hyperledger Sawtooth and Kubernetes at Hyperledger Hong Kong meetup. (1:38:24, Duncan Johnston-Watt, Blockchain Technology Partners, 2018)
    https://www.youtube.com/watch?v=d4tf5Ps4VLw
    Slides: https://bit.ly/2PR1Oub

* Introducción a Hyperledger VII - Sawtooth (Español) (7:36, Sergio Torres, Blocknitive)
    https://www.youtube.com/watch?v=b-VVNLce6MI

* ¿Qué es Hyperledger Sawtooth? (Español) (2:00, Angel Berniz)
    https://www.youtube.com/watch?v=_YkKaDXLVPg

### 2017 YouTube Videos
* Vision for Hyperledger's Sawtooth Distributed Ledger (2:03, Dan Middleton, Intel, 2017)
    https://www.youtube.com/watch?v=gjAHjX0RmOw
* Introduction to Hyperledger Sawtooth (Seafood Supply Chain) (3:40, Hyperledger, 2017)
    https://www.youtube.com/watch?v=8nrVlICgiYM

### Hyperledger Videos
* Hyperledger Sawtooth 1.0: Market Significance and Technical Overview. Free registration required (61:27, Dan Middleton, Intel, 2018)
    https://gateway.on24.com/wcc/gateway/linux/1101876/1585244/hyperledger-sawtooth-v10-market-significance-and-technical-overview

### Intel Chip Chat Audio
* Why Enterprises Should Be Moving Blockchain Forward. Ep. 576 (9:51, Mike Reed, Intel, 2018)
    https://connectedsocialmedia.com/16399/why-enterprises-should-be-moving-blockchain-forward-intel-chip-chat-episode-576/
* Where We've Been and Where We're going -- Intel's Blockchain Journey. Ep. 559 (11:05, Mike Reed, Intel, 2017)
    https://connectedsocialmedia.com/16112/where-weve-been-and-where-were-going-intels-blockchain-journey-intel-chip-chat-episode-559/


[Prev](sawtooth_faq3.md) [Next](sawtooth_notes.md)

© Copyright 2018, Intel Corporation.

© Portions Copyright 2018, Chainbelow Inc