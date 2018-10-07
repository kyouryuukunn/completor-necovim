if exists('g:loaded_completor_necovim_plugin')
  finish
endif

let g:loaded_completor_necovim_plugin = 1
let s:py = has('python3') ? 'py3' : 'py'


function! s:err(msg)
  echohl Error
  echo a:msg
  echohl NONE
endfunction


function! s:import_python()
  try
    exe s:py 'import completor_necovim'
  catch /^Vim(py\(thon\|3\)):/
    call s:err('Fail to import completor_necovim')
    return
  endtry

  try
    exe s:py 'import completor, completers.common'
  catch /^Vim(py\(thon\|3\)):/
    call s:err('Fail to import completor')
    return
  endtry

  try
    exe s:py 'completor.get("common").hooks.append(completor_necovim.Necovim.filetype)'
  catch /^Vim(py\(thon\|3\)):/
    call s:err('Fail to add necovim hook')
  endtry
endfunction


function! s:enable()
  call s:import_python()
  call s:disable()
endfunction


function! s:disable()
  augroup completor_necovim
    autocmd!
  augroup END
endfunction


augroup completor_necovim
  autocmd!
  autocmd InsertEnter * call s:enable()
augroup END
