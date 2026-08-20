import { assertParamsObject } from "@platforma-sdk/block-kind";
import { isPlRef } from "@platforma-sdk/model";
import { isBoolean, isString } from "es-toolkit";
import { isNumber } from "es-toolkit/compat";
import type { BlockParams } from "./types";

/**
 * The contract at runtime, for params that arrive from a template file rather
 * than from typed code.
 *
 * Each field the contract names is read and checked; a key it does not name is
 * dropped by never being read, so it needs no rejection here. Params written
 * against a different version of the contract are caught by the version in the
 * template entry's `{name}@{selector}` reference, not by a key-set check.
 */
export function parseInitializationParams(value: unknown): BlockParams {
  assertParamsObject(value);

  const params: Record<string, unknown> = {};
  for (const [field, { is, must }] of Object.entries(CONTRACT)) {
    const raw = value[field];
    if (raw === undefined) continue;
    if (!is(raw)) throw new Error(`'${field}' must be ${must}.`);
    params[field] = raw;
  }
  // Every value placed here passed its own field's guard, and `CONTRACT` is
  // proven exhaustive over `BlockParams` by the `satisfies` below.
  return params as BlockParams;
}

// ---------------------------------------------------------------------------
// Internals
// ---------------------------------------------------------------------------

type Guard<T> = (value: unknown) => value is T;

/** A guard plus how to finish the sentence "'field' must be …". */
type Check<T> = { readonly is: Guard<T>; readonly must: string };

function check<T>(is: Guard<T>, must: string): Check<T> {
  return { is, must };
}

const REF = "a reference to another block's output";

/**
 * The contract, field by field, at runtime.
 *
 * `datasetRef` is checked with `isPlRef` rather than a restatement of the shape,
 * so a hand-written entry is held to exactly what the rest of the system calls a
 * reference — including the `__isRef` marker the block dependency tree is
 * rebuilt from, whose absence would produce a block wired to nothing.
 *
 * `numPoints` and `numIterations` are checked only as strings, which is what the
 * block stores: the UI binds them to text inputs, so a half-typed value is an
 * ordinary state, and the block's own `args` is what holds them to whole numbers
 * under 10000. Rejecting a non-numeric string here would refuse a state the
 * editor reaches and can export.
 *
 * The `satisfies` clause is the drift guard: it demands an entry for every key
 * `BlockParams` declares, and types each guard against that key's own type. Add
 * a field to the contract and this stops compiling until the check exists —
 * which matters here because every field is optional, so a parser that simply
 * forgot one would otherwise return a valid `BlockParams` and say nothing.
 */
const CONTRACT = {
  datasetRef: check(isPlRef, REF),

  numPoints: check(isString, "a string"),
  numIterations: check(isString, "a string"),
  extrapolation: check(isBoolean, "a boolean"),

  mem: check(isNumber, "a number"),
  cpu: check(isNumber, "a number"),

  datasetLabel: check(isString, "a string"),
  customBlockLabel: check(isString, "a string"),
} satisfies { [K in keyof BlockParams]-?: Check<NonNullable<BlockParams[K]>> };
