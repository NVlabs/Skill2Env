# Migrating from Apollo Kotlin 4

Follow this order. Earlier steps unblock later ones (e.g. you can't compile to find runtime call-site errors until the Gradle plugin coordinates are right).

Confirm the user is on v4.

If the user is on v3 or earlier (group `com.apollographql.apollo3` or `com.apollographql.apollo` at `3.x`/`2.x`), they must migrate to v4 first using the [v3 → v4 migration guide](https://www.apollographql.com/docs/kotlin/migration/4.0); this skill only covers the v4 → v5 step.

Bump versions and plugin coordinates. Use the latest 5.x; run [../scripts/list-apollo-kotlin-versions.sh](scripts/list-apollo-kotlin-versions.sh) to discover it.

Build your project. If everything builds, the migration is over.

If you were using experimental (Data Builders, compiler plugins) or deprecated features (`ApolloIdlingResource`, `@nonnull`), you have to update them. Refer to the [Apollo Kotlin 5.0 migration guide](https://www.apollographql.com/docs/kotlin/migration/5.0) for details.

