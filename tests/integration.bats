#! /usr/bin/env bats

@test "minimal-patch" {
    run conventional_semver -s "fix: test"
    [ "$status" -eq 0 ]
    [ "$output" = "0.0.1" ]
}

@test "minimal-minor" {
    run conventional_semver -s "feat: test"
    [ "$status" -eq 0 ]
    [ "$output" = "0.1.0" ]
}

@test "minimal-major" {
    run conventional_semver -s "feat!: test"
    [ "$status" -eq 0 ]
    [ "$output" = "1.0.0" ]
}

@test "minimal-breaking" {
    run \
      conventional_semver -s "feat: test
    
      BREAKING CHANGE: this breaks"
    [ "$status" -eq 0 ]
    [ "$output" = "1.0.0" ]
}

@test "patch-with-version" {
    run conventional_semver -s --semver 1.0.3 "fix: test"
    [ "$status" -eq 0 ]
    [ "$output" = "1.0.4" ]
}

@test "minor-with-version" {
    run conventional_semver -s --semver 1.0.3 "feat: test"
    [ "$status" -eq 0 ]
    [ "$output" = "1.1.0" ]
}

@test "major-with-version" {
    run conventional_semver -s --semver 1.0.3 "feat!: test"
    [ "$status" -eq 0 ]
    [ "$output" = "2.0.0" ]
}

@test "breaking-with-version" {
    run \
      conventional_semver -s --semver 1.0.3 "feat: test
      
      BREAKING CHANGE: this breaks"
    [ "$status" -eq 0 ]
    [ "$output" = "2.0.0" ]
}
