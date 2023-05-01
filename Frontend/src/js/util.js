
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


/**
 * Checks if an object has values
 *
 * @export
 * @param {*} source object
 * @param {string[]} values List of properties
 */
export function hasValues(source, values) {
  for(const prop of values) {
    if(source[prop] == undefined || source[prop] == null || source[prop] === "") return false
  }
  return true
}
