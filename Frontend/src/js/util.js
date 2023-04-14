
/**
 * Shallow copies an object onto another
 *
 * @export
 * @param {*} source
 * @param {*} dest
 */
export function copyObject(source, dest) {
  for(let prop in source) {
    dest[prop] = source[prop]
  }
}
