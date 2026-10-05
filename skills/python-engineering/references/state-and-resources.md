# State, resources, and persisted outcomes

Read this when a change affects checkpoint recovery, owned clients/models, lifecycle, or artifact publication.

## Make the lifecycle visible

Identify the source of truth and the states the consumer can actually encounter. Distinguish fresh, partially completed, completed, invalid, and unavailable state only where those distinctions change behavior. Represent mutually exclusive outcomes explicitly instead of allowing a pile of optional fields to encode contradictory states.

Trace acquisition, restoration, use, export/publication, and cleanup at the composition boundary. Keep the resource that owns mutable state identifiable. A step counter or completion marker is not a substitute for loading the state it describes.

Use a context manager or explicit `try/finally` when the API supports it. Release owned resources on normal and exceptional paths without discarding the original failure. Caller-owned resources should follow the ownership contract rather than being closed unexpectedly.

## Define recovery and publication semantics

Settle which checkpoint/result is authoritative, what happens when it is absent, and whether success means computation finished or a consumer-visible artifact was published. Follow existing library semantics unless the task authorizes a change.

Specify reuse identity where expensive effects are involved. A record identifier may be insufficient if the prompt, model, preprocessing, or configuration changes the meaning of a result. Do not invent an identity scheme or silently invalidate historical artifacts without a contract.

When consumers require complete artifacts, write to an appropriate temporary destination and publish using the storage system's supported atomic operation or explicit completion protocol. Filesystem replacement is not a universal transaction across files or remote stores. Verify failure behavior at the relevant boundary and preserve an earlier valid result when the contract requires it.

## Keep verification connected

Exercise the path from selected state through the actual orchestrator to the consumed artifact. Observe state values or artifact identity, not merely a skipped method call. Check release after failures that can occur after acquisition.

Use realistic boundary substitutes for bounded CPU checks, and separately identify real-runtime behavior still needing a canary. The goal is a few strong observations of the risky transitions, not a test for every method.
