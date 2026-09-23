flowchart LR
    subgraph Resolver
        Edge["TAPIR Edge<br/>- minimering<br/>- anonymisering<br/>av DNS TAP"]
    end

    Aggregat["Aggregat"]
    Events["Events"]
    Core[("TAPIR Core")]
    ThirdParty["3:e part"]

    Edge --> Aggregat
    Edge --> Events
    Aggregat --> Core
    Events --> Core
    Core --> ThirdParty