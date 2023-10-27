;;(load "~/etc/edit-server.el")
;;(require 'edit-server)
;;(edit-server-start)

;;(load "~/etc/python-mode.el")
(set-frame-height (selected-frame) 44)
(set-frame-width (selected-frame) 172)
(set-frame-position (selected-frame) 15 20)

;;(set-frame-height (selected-frame) 65)
;;(set-frame-width (selected-frame) 224)
;;(setq inhibit-terminal-defaults t)
;;(setq default-fill-column 102)
(setq default-major-mode 'text-mode)
(set-background-color "antique white")
(set-foreground-color "navy blue")
(set-cursor-color "red")
(require 'python-mode "~/etc/python-mode.elc")
(require 'gs-mode "~/etc/gs-mode.el")
(require 'ctl-mode "~/etc/ctl-mode.el")

;;;;(setq load-path (cons "~/etc" load-path))

;;;;;(setq auto-mode-alist (append (list (cons "\\.pl$" 'perl-mode)) auto-mode-alist))
(setq auto-mode-alist (append (list (cons "\\.xml$" 'indented-text-mode)) auto-mode-alist))

;;
;; 20030306 -- modified /usr/share/emacs/site-list/sh-script.el
;;
(setq auto-mode-alist (append (list (cons "\\.csh$" 'text-mode)) auto-mode-alist))
(setq auto-mode-alist (append (list (cons "\\.sh$" 'text-mode)) auto-mode-alist))
(setq auto-mode-alist (append (list (cons "\\.f90$" 'f90-mode)) auto-mode-alist))

(setq auto-mode-alist (append (list (cons "\\.exp$" 'c-mode)) auto-mode-alist))
(setq auto-mode-alist (append (list (cons "\\.c$" 'perl-mode)) auto-mode-alist))
(setq auto-mode-alist (append (list (cons "\\.h$" 'perl-mode)) auto-mode-alist))
(setq auto-mode-alist (append (list (cons "Makefile$" 'text-mode)) auto-mode-alist))
(setq auto-mode-alist (append (list (cons "Makefile.in$" 'text-mode)) auto-mode-alist))
(setq auto-mode-alist (append (list (cons "\\.htm$" 'text-mode)) auto-mode-alist))
;(setq auto-mode-alist (append (list (cons "\\.html$" 'text-mode)) auto-mode-alist))
(setq auto-mode-alist (append (list (cons "\\.emacs$" 'text-mode)) auto-mode-alist))
(setq auto-mode-alist (append (list (cons "\\.login$" 'text-mode)) auto-mode-alist))

;(setq auto-mode-alist (cons '("\\.py$" . python-mode) auto-mode-alist))
;(setq interpreter-mode-alist (cons '("python" . python-mode)
;                                            interpreter-mode-alist))
;(autoload 'python-mode "python-mode" "Python editing mode." t)
         

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; File name: ` ~/.emacs '
;;; ---------------------
;;;
;;; Note: This file switches between two Emacs versions:
;;;            GNU-Emacs (19.34/20.X) and X-Emacs (19.14/20.X).
;;;       Please to not mix both versions: GNU-Emacs and X-Emacs
;;;       are incompatible. They use differnet binary code for
;;;       compiled lisp files and they have different builtin
;;;       lisp functions ... not only names of such functions
;;;       are different!!!
;;;
;;; If you need your own personal ~/.emacs
;;; please make a copy of this file
;;; an placein your changes and/or extension.
;;;
;;; Copyright (c) 1997 S.u.S.E. Gmbh Fuerth, Germany.  All rights reserved.
;;;
;;; Author: Werner Fink, <werner@suse.de> 1997,98,99
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;
;;; Test of Emacs derivates
;;; -----------------------
(if (string-match "XEmacs\\|Lucid" emacs-version)
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;;; XEmacs
  ;;; ------
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  (progn
      ;;
      ;; If not exists create the XEmacs options file
      ;; --------------------------------------------
      (if (and (not (file-readable-p "~/.xemacs-options"))
	       (fboundp 'save-options-menu-settings))
	(save-options-menu-settings))
      ;;
      ;; Remember font and more settings
      ;; -------------------------------
      (setq options-save-faces t)
      ;;
      ;; AUC-TeX
      ;; -------
      (if  (or (file-accessible-directory-p
	        "/usr/X11R6/lib/xemacs/site-lisp/auctex/")
       		(or (and (= emacs-major-version 19)
			 (>= emacs-minor-version 15))
           	    (= emacs-major-version 20)))
       (progn
	   (require 'tex-site)
	   (setq-default TeX-master nil)
	   ; Users private libaries 
	   ; (setq TeX-macro-private '("~/lib/tex-lib/"))
	   ;    AUC-TeX-Macros
	   ; (setq TeX-style-private   "~/lib/xemacs/site-lisp/auctex/style/")
	   ;    Autom. Auc-TeX-Macros
	   ; (setq TeX-auto-private    "~/lib/xemacs/site-lisp/auctex/auto/")
	))
  )
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;;; GNU-Emacs
  ;;; ---------
  ;;; load ~/.gnu-emacs or, if not exists /etc/skel/.gnu-emacs
  ;;; For a description and the settings see /etc/skel/.gnu-emacs
  ;;;   ... for your private ~/.gnu-emacs your are on your one.
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  (if (file-readable-p "~/.gnu-emacs")
      (load "~/.gnu-emacs" nil t)
    (if (file-readable-p "/etc/skel/.gnu-emacs")
	(load "/etc/skel/.gnu-emacs" nil t)))

  ;; Custum Settings
  ;; ===============
  ;; To avoid any trouble with the customization system of GNU emacs
  ;; we set the default file ~/.gnu-emacs-custom
  (setq custom-file "~/.gnu-emacs-custom")
  (load "~/.gnu-emacs-custom" t t)
;;;
)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; XEmacs load options
;;; -------------------
;;; If missing the next few lines they will be append automatically
;;; by xemacs. This will be done by `save-options-menu-settings'
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; Custum Settings
;; ===============
;; Set custom-file to ~/.xemacs-custom for XEmacs to avoid overlap with the
;; custom interface of GNU-Emacs. Nevertheless, in most cases GNU-Emacs can
;; not handle unknown functions in ~/.emacs .. therefore ~/.xemacs-custom.
(cond
 ((string-match "XEmacs" emacs-version)
	(setq custom-file "~/.xemacs-custom")
	(load "~/.xemacs-custom" t t)))
;; ======================
;; End of Custum Settings

;; Options Menu Settings
;; =====================
(cond
 ((and (string-match "XEmacs" emacs-version)
       (boundp 'emacs-major-version)
       (or (and
            (= emacs-major-version 19)
            (>= emacs-minor-version 14))
           (= emacs-major-version 20))
       (fboundp 'load-options-file))
  (load-options-file "~/.xemacs-options")))
;; ============================
;; End of Options Menu Settings

         

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; File name: ` ~/.emacs '
;;; ---------------------
;;;
;;; Note: This file switches between two Emacs versions:
;;;            GNU-Emacs (19.34/20.X) and X-Emacs (19.14/20.X).
;;;       Please to not mix both versions: GNU-Emacs and X-Emacs
;;;       are incompatible. They use differnet binary code for
;;;       compiled lisp files and they have different builtin
;;;       lisp functions ... not only names of such functions
;;;       are different!!!
;;;
;;; If you need your own personal ~/.emacs
;;; please make a copy of this file
;;; an placein your changes and/or extension.
;;;
;;; Copyright (c) 1997 S.u.S.E. Gmbh Fuerth, Germany.  All rights reserved.
;;;
;;; Author: Werner Fink, <werner@suse.de> 1997,98,99
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;
;;; Test of Emacs derivates
;;; -----------------------
(if (string-match "XEmacs\\|Lucid" emacs-version)
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;;; XEmacs
  ;;; ------
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  (progn
      ;;
      ;; If not exists create the XEmacs options file
      ;; --------------------------------------------
      (if (and (not (file-readable-p "~/.xemacs-options"))
	       (fboundp 'save-options-menu-settings))
	(save-options-menu-settings))
      ;;
      ;; Remember font and more settings
      ;; -------------------------------
      (setq options-save-faces t)
      ;;
      ;; AUC-TeX
      ;; -------
      (if  (or (file-accessible-directory-p
	        "/usr/X11R6/lib/xemacs/site-lisp/auctex/")
       		(or (and (= emacs-major-version 19)
			 (>= emacs-minor-version 15))
           	    (= emacs-major-version 20)))
       (progn
	   (require 'tex-site)
	   (setq-default TeX-master nil)
	   ; Users private libaries 
	   ; (setq TeX-macro-private '("~/lib/tex-lib/"))
	   ;    AUC-TeX-Macros
	   ; (setq TeX-style-private   "~/lib/xemacs/site-lisp/auctex/style/")
	   ;    Autom. Auc-TeX-Macros
	   ; (setq TeX-auto-private    "~/lib/xemacs/site-lisp/auctex/auto/")
	))
  )
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;;; GNU-Emacs
  ;;; ---------
  ;;; load ~/.gnu-emacs or, if not exists /etc/skel/.gnu-emacs
  ;;; For a description and the settings see /etc/skel/.gnu-emacs
  ;;;   ... for your private ~/.gnu-emacs your are on your one.
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  (if (file-readable-p "~/.gnu-emacs")
      (load "~/.gnu-emacs" nil t)
    (if (file-readable-p "/etc/skel/.gnu-emacs")
	(load "/etc/skel/.gnu-emacs" nil t)))

  ;; Custum Settings
  ;; ===============
  ;; To avoid any trouble with the customization system of GNU emacs
  ;; we set the default file ~/.gnu-emacs-custom
  (setq custom-file "~/.gnu-emacs-custom")
  (load "~/.gnu-emacs-custom" t t)
;;;
)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; XEmacs load options
;;; -------------------
;;; If missing the next few lines they will be append automatically
;;; by xemacs. This will be done by `save-options-menu-settings'
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; Custum Settings
;; ===============
;; Set custom-file to ~/.xemacs-custom for XEmacs to avoid overlap with the
;; custom interface of GNU-Emacs. Nevertheless, in most cases GNU-Emacs can
;; not handle unknown functions in ~/.emacs .. therefore ~/.xemacs-custom.
(cond
 ((string-match "XEmacs" emacs-version)
	(setq custom-file "~/.xemacs-custom")
	(load "~/.xemacs-custom" t t)))
;; ======================
;; End of Custum Settings

;; Options Menu Settings
;; =====================
(cond
 ((and (string-match "XEmacs" emacs-version)
       (boundp 'emacs-major-version)
       (or (and
            (= emacs-major-version 19)
            (>= emacs-minor-version 14))
           (= emacs-major-version 20))
       (fboundp 'load-options-file))
  (load-options-file "~/.xemacs-options")))
;; ============================
;; End of Options Menu Settings
;(setq auto-mode-alist (cons "\\.F\\'" . fortran-mode))
;                              auto-mode-alist))
;
; Turn on color highlighting
;
;From jimf%saber@harvard.harvard.edu Wed Jan 31 21:16:36 1990
;Date: Wed, 31 Jan 90 19:36:26 EST
;From: jimf%saber@harvard.harvard.edu (Jim Frost)
;To: dsill@relay
;Subject: Emacs Lisp archives
;
;Someone suggested to me that I submit my wordstar.el emacs lisp file
;to the elisp archives.	 It looks like you're the target point for the
;archive.
;
;If this isn't the case, I'm sorry to bother you -- please just bounce
;this and tell me you're not the right person.	Otherwise, read on.
;
;What follows is a set of Emacs bindings that give a fair approximation
;of the WordStar 3.x key bindings, with a couple of extensions.	 It's
;good enough not to drive WordStar people crazy but I confess that I
;didn't work too hard on it (it shows -- nowadays I'd probably make it
;a mode or something).	If you want to include this in the archives, go
;ahead -- I just give it away to anyone who requests it anyway.
;
;Happy hacking,
;
;jim frost
;saber software
;jimf@saber.com
;
;-- cut here --
; Wordstar Keycap Definition for EMACS
;
; This file causes EMACS to emulate WordStar.  You should do one of
; two things to make this work.	 Either copy this file into ~/.emacs,
; after which it will be loaded every time you call up emacs, or
; copy it into ~/.wordstar and make an alias ws 'emacs -l ~/.wordstar'
; which will let you call it up with the "normal" ws command.
;
; caveats: * ^G (delete-character) is hard bound to the emacs function
;	     quit, so if you delete very fast you might cause emacs to
;	     abort.  tell it to save your file and then to continue and
;	     all will be well, although annoying.  this doesn't happen
;	     often unless the machine is kind of slow.
;	   * block copy and delete work as they do in emacs, not in
;	     wordstar, which means you can block end above the block
;	     begin and you can also block-delete from block begin to
;	     where the cursor is without explicitly doing a block-end.
;	   * ^Owv is split-window-vertically
;	   * ^Owh is split-window-horizontally
;	   * ^Owo is other-window
;	   * ^Owd is delete-other-windows
;
; for further information contact jim frost at madd@bu-it.bu.edu
;
(setq inhibit-terminal-defaults t)
(setq compile 'cft77)
(setq default-fill-column 72)
(setq default-major-mode 'text-mode)
(setq c-mode-hook
      '(lambda ()
        (define-key global-map "\003" 'scroll-up)))
(setq C-K-map (make-keymap))
(define-key C-K-map " " ())
(define-key C-K-map "b" 'set-mark-command)
(define-key C-K-map "\002" 'set-mark-command)
(define-key C-K-map "c" 'yank)
(define-key C-K-map "\003" 'yank)
(define-key C-K-map "d" 'save-buffers-kill-emacs)
(define-key C-K-map "\004" 'save-buffers-kill-emacs)
(define-key C-K-map "f" 'find-file)
(define-key C-K-map "\006" 'find-file)
(define-key C-K-map "k" 'copy-region-as-kill)
(define-key C-K-map "\013" 'copy-region-as-kill)
(define-key C-K-map "o" 'find-file)
(define-key C-K-map "\017" 'find-file)
(define-key C-K-map "q" 'kill-buffer)
(define-key C-K-map "\021" 'kill-buffer)
(define-key C-K-map "r" 'insert-file)
(define-key C-K-map "\022" 'insert-file)
(define-key C-K-map "s" 'save-some-buffers)
(define-key C-K-map "\023" 'save-some-buffers)
(define-key C-K-map "t" 'kill-rectangle)
(define-key C-K-map "\024" 'kill-rectangle)
(define-key C-K-map "\025" ())
(define-key C-K-map "v" 'yank)
(define-key C-K-map "\026" 'yank)
(define-key C-K-map "w" 'append-to-file)
(define-key C-K-map "\027" 'append-to-file)
(define-key C-K-map "y" 'kill-region)
(define-key C-K-map "\031" 'kill-region)

(setq C-O-map (make-keymap))
(define-key C-O-map " " ())
(define-key C-O-map "c" 'center-line)
(define-key C-O-map "\003" 'center-line)
(define-key C-O-map "b" 'switch-to-buffer)
(define-key C-O-map "\002" 'switch-to-buffer)
(define-key C-O-map "j" 'justify-current-line)
(define-key C-O-map "\012" 'justify-current-line)
(define-key C-O-map "k" 'kill-buffer)
(define-key C-O-map "\013" 'kill-buffer)
(define-key C-O-map "l" 'list-buffers)
(define-key C-O-map "\014" 'list-buffers)
(define-key C-O-map "m" 'auto-fill-mode)
(define-key C-O-map "\015" 'auto-fill-mode)
(define-key C-O-map "r" 'set-fill-column)
(define-key C-O-map "\022" 'set-fill-column)
(define-key C-O-map "\025" ())
(define-key C-O-map "fc" 'compile)
(define-key C-O-map "fn" 'next-error)
(define-key C-O-map "wd" 'delete-other-windows)
(define-key C-O-map "wh" 'split-window-horizontally)
(define-key C-O-map "wo" 'other-window)
(define-key C-O-map "wv" 'split-window-vertically)

(setq C-Q-map (make-keymap))
(define-key C-Q-map " " ())
(define-key C-Q-map "a" 'query-replace)
(define-key C-Q-map "\001" 'query-replace)
(define-key C-Q-map "b" 'beginning-of-line)
(define-key C-Q-map "\002" 'beginning-of-line)
(define-key C-Q-map "c" 'end-of-buffer)
(define-key C-Q-map "\003" 'end-of-buffer)
(define-key C-Q-map "e" 'end-of-line)
(define-key C-Q-map "\005" 'end-of-line)
(define-key C-Q-map "f" 're-search-forward)
(define-key C-Q-map "\006" 're-search-forward)

(define-key C-Q-map "l" 'goto-line)
(define-key C-Q-map "\014" 'goto-line)
(define-key C-Q-map "r" 'beginning-of-buffer)
(define-key C-Q-map "\022" 'beginning-of-buffer)
(define-key C-Q-map "\025" ())
(define-key C-Q-map "y" 'kill-line)
(define-key C-Q-map "\031" 'kill-line)
(define-key C-Q-map "jk" 'bookmark-set)
(define-key C-Q-map "jj" 'bookmark-jump)


(define-key global-map "\001" 'backward-word)
(define-key global-map "\002" 'fill-paragraph)
(define-key global-map "\003" 'scroll-up)
(global-set-key "\C-c" 'scroll-up)
(define-key global-map "\004" 'forward-char)
(define-key global-map "\005" 'previous-line)
(define-key global-map "\006" 'forward-word)
(define-key global-map "\007" 'delete-char)
(define-key global-map "\010" 'delete-backward-char)
(define-key global-map "\011" 'indent-for-tab-command)
(define-key global-map "\012" 'help-for-help)
(define-key global-map "\013" C-K-map)
(define-key global-map "\014" 'repeat-complex-command)
(define-key global-map "\016" 'newline)
(define-key global-map "\017" C-O-map)
(define-key global-map "\020" 'quoted-insert)
(define-key global-map "\021" C-Q-map)
(define-key global-map "\022" 'scroll-down)
(define-key global-map "\023" 'backward-char)
(define-key global-map "\024" 'kill-word)
(define-key global-map "\025" 'undo)
(define-key global-map "\026" 'overwrite-mode)
(define-key global-map "\027" 'previous-line)
(global-set-key "\C-x" 'previous-line)
(define-key global-map "\030" 'next-line)
(define-key global-map "\031" '(lambda () (interactive)
				(beginning-of-line)
				(delete-region (point)
					       (progn (forward-line 1)
						      (point)))))
(define-key global-map "\035" 'quoted-insert)
(define-key global-map "\037" C-Q-map)

;;
;; overide C-c prefix in C mode
;;

(setq shell-script-mode-hook
     '(lambda ()
	(define-key shell-script-mode-map "\C-c" 'nil)
	))

(setq latex-mode-hook
      '(lambda ()
	(define-key latex-mode-map "\C-c" 'nil)
	))

(setq tex-mode-hook
      '(lambda ()
	(define-key tex-mode-map "\C-c" 'nil)
	))

(setq f90-mode-hook
      '(lambda ()
	(define-key f90-mode-map "\C-c" 'nil)
	))

(setq bibtex-mode-hook
      '(lambda ()
	(define-key bibtex-mode-map "\C-c" 'nil)
	))

(setq c-mode-hook
      '(lambda ()
	(define-key c-mode-map "\C-d" 'nil)
	))

(setq python-mode-hook
      '(lambda ()
	(define-key py-mode-map "\e\C-x" 'nil)
	))

(setq php-mode-hook
      '(lambda ()
      (define-key php-mode-map "\C-c" 'nil)
      ))


(setq lisp-mode-hook
      '(lambda ()
	(define-key lisp-mode-map "\C-c" 'nil)
	))

(setq html-mode-hook
      '(lambda ()
	(define-key html-mode-map "\C-c" 'scroll-up)
	))

(setq Makefile-mode-hook
      '(lambda ()
	(define-key Makefile-mode-map "\C-c" 'nil)
	))

;;
;; overide C-c prefix in text mode
;;
(define-key text-mode-map "\C-c" 'nil)


;; USMID @(#)emacs/lisp/fortran.el	1.1	08/28/90 17:05:41
;;; Fortran mode for GNU Emacs  (beta test version 1.21, Oct. 1, 1985)
;;; Copyright (c) 1986 Free Software Foundation, Inc.
;;; Written by Michael D. Prange (mit-eddie!mit-erl!prange).

;;; This file is not part of the GNU Emacs distribution (yet).

;; This file is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY.  No author or distributor
;; accepts responsibility to anyone for the consequences of using it
;; or for whether it serves any particular purpose or works at all,
;; unless he says so in writing.  Refer to the GNU Emacs General Public
;; License for full details.

;; Everyone is granted permission to copy, modify and redistribute
;; this file, but only under the conditions described in the
;; GNU Emacs General Public License.   A copy of this license is
;; supposed to have been given to you along with GNU Emacs so you
;; can know your rights and responsibilities.  It should be in a
;; file named COPYING.  Among other things, the copyright notice
;; and this notice must be preserved on all copies.

;;; Author acknowledges help from Stephen Gildea <mit-erl!gildea>

;;; Bugs to mit-erl!bug-fortran-mode.

(defvar fortran-do-indent 2
  "*Extra indentation applied to `do' blocks.")

(defvar fortran-if-indent 2
  "*Extra indentation applied to `if' blocks.")

(defvar fortran-continuation-indent 5
  "*Extra indentation applied to `continuation' lines.")

(defvar fortran-comment-indent-style 'fixed
  "*nil forces comment lines not to be touched,
'fixed produces fixed comment indentation to comment-column,
and 'relative indents to current fortran indentation plus comment-column.")

(defvar fortran-comment-line-column 10
  "*Indentation for text in comment lines.")

(defvar comment-line-start nil
  "*Delimiter inserted to start new full-line comment.")

(defvar comment-line-start-skip nil
  "*Regexp to match the start of a full-line comment.")

(defvar fortran-minimum-statement-indent 6
  "*Minimum indentation for fortran statements.")

;; Note that this is documented in the v18 manuals as being a string
;; of length one rather than a single character.
;; The code in this file accepts either format for compatibility.
(defvar fortran-comment-indent-char ? 
  "*Character to be inserted for Fortran comment indentation.
Normally a space.")

(defvar fortran-line-number-indent 1
  "*Maximum indentation for Fortran line numbers.
5 means right-justify them within their five-column field.")

(defvar fortran-check-all-num-for-matching-do 1
  "*Non-nil causes all numbered lines to be treated as possible do-loop ends.")

(defvar fortran-continuation-char ?$
  "*Character which is inserted in column 5 by \\[fortran-split-line]
to begin a continuation line.  Normally $.")

(defvar fortran-comment-region "c$$$"
  "*String inserted by \\[fortran-comment-region] at start of each line in region.")

(defvar fortran-electric-line-number t
  "*Non-nil causes line number digits to be moved to the correct column as typed.")

(defvar fortran-electric-tab-carriage-return t
  "*Non-nil causes lines to be automaticaly indented by hitting a carriage return .")

(defvar fortran-startup-message t
  "*Non-nil displays a startup message when fortran-mode is first called.")

(defvar fortran-column-ruler
  (concat "0   4 6  10        20        30        40        50        60        70\n"
	  "[   ]|{   |    |    |    |    |    |    |    |    |    |    |    |    |}\n")
  "*String displayed above current line by \\[fortran-column-ruler].")

(defconst fortran-mode-version "1.21")

(defvar fortran-mode-syntax-table nil
  "Syntax table in use in fortran-mode buffers.")

(if fortran-mode-syntax-table
    ()
  (setq fortran-mode-syntax-table (make-syntax-table))
  (modify-syntax-entry ?\; "w" fortran-mode-syntax-table)
  (modify-syntax-entry ?+ "." fortran-mode-syntax-table)
  (modify-syntax-entry ?- "." fortran-mode-syntax-table)
  (modify-syntax-entry ?* "." fortran-mode-syntax-table)
  (modify-syntax-entry ?/ "." fortran-mode-syntax-table)
  (modify-syntax-entry ?\' "\"" fortran-mode-syntax-table)
  (modify-syntax-entry ?\" "\"" fortran-mode-syntax-table)
  (modify-syntax-entry ?\\ "/" fortran-mode-syntax-table)
  (modify-syntax-entry ?. "w" fortran-mode-syntax-table)
  (modify-syntax-entry ?\n ">" fortran-mode-syntax-table))

(defvar fortran-mode-map () 
  "Keymap used in fortran mode.")

(if fortran-mode-map
    ()
  (setq fortran-mode-map (make-sparse-keymap))
  (define-key fortran-mode-map ";" 'fortran-abbrev-start)
  (define-key fortran-mode-map "\C-p;" 'fortran-comment-region)
  (define-key fortran-mode-map "\e\C-a" 'beginning-of-fortran-subprogram)
  (define-key fortran-mode-map "\e\C-e" 'end-of-fortran-subprogram)
  (define-key fortran-mode-map "\e;" 'fortran-indent-comment)
  (define-key fortran-mode-map "\e\C-h" 'mark-fortran-subprogram)
  (define-key fortran-mode-map "\e\n" 'fortran-split-line)
  (define-key fortran-mode-map "\e\C-q" 'fortran-indent-subprogram)
  (define-key fortran-mode-map "\C-p\C-c" 'compile)
  (define-key fortran-mode-map "\C-p\C-w" 'fortran-window-create)
  (define-key fortran-mode-map "\C-p\C-r" 'fortran-column-ruler)
  (define-key fortran-mode-map "\C-p\C-p" 'fortran-previous-statement)
  (define-key fortran-mode-map "\C-p\C-n" 'fortran-next-statement)
  (define-key fortran-mode-map "\t" 'fortran-indent-line)
  (define-key fortran-mode-map "\C-m" 'fortran-electric-tab-carriage-return)
  (define-key fortran-mode-map "0" 'fortran-electric-line-number)
  (define-key fortran-mode-map "1" 'fortran-electric-line-number)
  (define-key fortran-mode-map "2" 'fortran-electric-line-number)
  (define-key fortran-mode-map "3" 'fortran-electric-line-number)
  (define-key fortran-mode-map "4" 'fortran-electric-line-number)
  (define-key fortran-mode-map "5" 'fortran-electric-line-number)
  (define-key fortran-mode-map "6" 'fortran-electric-line-number)
  (define-key fortran-mode-map "7" 'fortran-electric-line-number)
  (define-key fortran-mode-map "8" 'fortran-electric-line-number)
  (define-key fortran-mode-map "9" 'fortran-electric-line-number))

(defvar fortran-mode-abbrev-table nil)
(if fortran-mode-abbrev-table
    ()
  (define-abbrev-table 'fortran-mode-abbrev-table ())
  (let ((abbrevs-changed nil))
    (define-abbrev fortran-mode-abbrev-table  ";b"   "byte" nil)
    (define-abbrev fortran-mode-abbrev-table  ";ch"  "character" nil)
    (define-abbrev fortran-mode-abbrev-table  ";cl"  "close" nil)
    (define-abbrev fortran-mode-abbrev-table  ";c"   "continue" nil)
    (define-abbrev fortran-mode-abbrev-table  ";cm"  "common" nil)
    (define-abbrev fortran-mode-abbrev-table  ";cx"  "complex" nil)
    (define-abbrev fortran-mode-abbrev-table  ";di"  "dimension" nil)
    (define-abbrev fortran-mode-abbrev-table  ";do"  "double" nil)
    (define-abbrev fortran-mode-abbrev-table  ";dc"  "double complex" nil)
    (define-abbrev fortran-mode-abbrev-table  ";dp"  "double precision" nil)
    (define-abbrev fortran-mode-abbrev-table  ";dw"  "do while" nil)
    (define-abbrev fortran-mode-abbrev-table  ";e"   "else" nil)
    (define-abbrev fortran-mode-abbrev-table  ";ed"  "enddo" nil)
    (define-abbrev fortran-mode-abbrev-table  ";el"  "elseif" nil)
    (define-abbrev fortran-mode-abbrev-table  ";en"  "endif" nil)
    (define-abbrev fortran-mode-abbrev-table  ";eq"  "equivalence" nil)
    (define-abbrev fortran-mode-abbrev-table  ";ex"  "external" nil)
    (define-abbrev fortran-mode-abbrev-table  ";ey"  "entry" nil)
    (define-abbrev fortran-mode-abbrev-table  ";f"   "format" nil)
    (define-abbrev fortran-mode-abbrev-table  ";fu"  "function" nil)
    (define-abbrev fortran-mode-abbrev-table  ";g"   "goto" nil)
    (define-abbrev fortran-mode-abbrev-table  ";im"  "implicit" nil)
    (define-abbrev fortran-mode-abbrev-table  ";ib"  "implicit byte" nil)
    (define-abbrev fortran-mode-abbrev-table  ";ic"  "implicit complex" nil)
    (define-abbrev fortran-mode-abbrev-table  ";ich" "implicit character" nil)
    (define-abbrev fortran-mode-abbrev-table  ";ii"  "implicit integer" nil)
    (define-abbrev fortran-mode-abbrev-table  ";il"  "implicit logical" nil)
    (define-abbrev fortran-mode-abbrev-table  ";ir"  "implicit real" nil)
    (define-abbrev fortran-mode-abbrev-table  ";inc" "include" nil)
    (define-abbrev fortran-mode-abbrev-table  ";in"  "integer" nil)
    (define-abbrev fortran-mode-abbrev-table  ";intr" "intrinsic" nil)
    (define-abbrev fortran-mode-abbrev-table  ";l"   "logical" nil)
    (define-abbrev fortran-mode-abbrev-table  ";op"  "open" nil)
    (define-abbrev fortran-mode-abbrev-table  ";pa"  "parameter" nil)
    (define-abbrev fortran-mode-abbrev-table  ";pr"  "program" nil)
    (define-abbrev fortran-mode-abbrev-table  ";p"   "print" nil)
    (define-abbrev fortran-mode-abbrev-table  ";re"  "real" nil)
    (define-abbrev fortran-mode-abbrev-table  ";r"   "read" nil)
    (define-abbrev fortran-mode-abbrev-table  ";rt"  "return" nil)
    (define-abbrev fortran-mode-abbrev-table  ";rw"  "rewind" nil)
    (define-abbrev fortran-mode-abbrev-table  ";s"   "stop" nil)
    (define-abbrev fortran-mode-abbrev-table  ";su"  "subroutine" nil)
    (define-abbrev fortran-mode-abbrev-table  ";ty"  "type" nil)
    (define-abbrev fortran-mode-abbrev-table  ";w"   "write" nil)))

(defun fortran-mode ()
  "Major mode for editing fortran code.
Tab indents the current fortran line correctly. 
`do' statements must not share a common `continue'.

Type `;?' or `;\\[help-command]' to display a list of built-in abbrevs for Fortran keywords.

Variables controlling indentation style and extra features:

 comment-start
    Normally nil in Fortran mode.  If you want to use comments
    starting with `!', set this to the string \"!\".
 fortran-do-indent
    Extra indentation within do blocks.  (default 3)
 fortran-if-indent
    Extra indentation within if blocks.  (default 3)
 fortran-continuation-indent
    Extra indentation appled to continuation statements.  (default 5)
 fortran-comment-line-column
    Amount of indentation for text within full-line comments. (default 6)
 fortran-comment-indent-style
    nil    means don't change indentation of text in full-line comments,
    fixed  means indent that text at column fortran-comment-line-column
    relative  means indent at fortran-comment-line-column beyond the
 	      indentation for a line of code.
    Default value is fixed.
 fortran-comment-indent-char
    Character to be inserted instead of space for full-line comment
    indentation.  (default SPC)
 fortran-minimum-statement-indent
    Minimum indentation for fortran statements. (default 6)
 fortran-line-number-indent
    Maximum indentation for line numbers.  A line number will get
    less than this much indentation if necessary to avoid reaching
    column 5.  (default 1)
 fortran-check-all-num-for-matching-do
    Non-nil causes all numbered lines to be treated as possible 'continue'
    statements.  (default 1)
 fortran-continuation-char
    character to be inserted in column 5 of a continuation line.
    (default $)
 fortran-comment-region
    String inserted by \\[fortran-comment-region] at start of each line in 
    region.  (default \"c$$$\")
 fortran-electric-line-number
    Non-nil causes line number digits to be moved to the correct column 
    as typed.  (default t)
 fortran-electric-tab-carriage-return
    Non-nil causes lines to be automaticaly indented to correct column 
    as typed.  (default t)
 fortran-startup-message
    Set to nil to inhibit message first time fortran-mode is used.

Turning on Fortran mode calls the value of the variable fortran-mode-hook 
with no args, if that value is non-nil.
\\{fortran-mode-map}"
  (interactive)
  (kill-all-local-variables)
  (if fortran-startup-message
      (message "Emacs Fortran mode version %s.  Bugs to mit-erl!bug-fortran-mode" fortran-mode-version))
  (setq fortran-startup-message nil)
  (setq local-abbrev-table fortran-mode-abbrev-table)
  (set-syntax-table fortran-mode-syntax-table)
  (make-local-variable 'indent-line-function)
  (setq indent-line-function 'fortran-indent-line)
  (make-local-variable 'comment-indent-hook)
  (setq comment-indent-hook 'fortran-comment-hook)
  (make-local-variable 'comment-line-start-skip)
  (setq comment-line-start-skip "^[Cc*][^ \t\n]*[ \t]*") ;[^ \t\n]* handles comment strings such as c$$$
  (make-local-variable 'comment-line-start)
  (setq comment-line-start "c")
  (make-local-variable 'comment-start-skip)
  (setq comment-start-skip "![ \t]*")
  (make-local-variable 'comment-start)
  (setq comment-start "!")
  (make-local-variable 'require-final-newline)
  (setq require-final-newline t)
  (make-local-variable 'abbrev-all-caps)
  (setq abbrev-all-caps t)
  (make-local-variable 'indent-tabs-mode)
  (setq indent-tabs-mode nil)
  (use-local-map fortran-mode-map)
  (setq mode-name "Fortran")
  (setq major-mode 'fortran-mode)
  (run-hooks 'fortran-mode-hook))

(defun fortran-comment-hook ()
  (save-excursion
    (skip-chars-backward " \t")
    (max (+ 1 (current-column))
	 comment-column)))

(defun fortran-indent-comment ()
  "Align or create comment on current line.
Existing comments of all types are recognized and aligned.
If the line has no comment, a side-by-side comment is inserted and aligned
if the value of  comment-start  is not nil.
Otherwise, a separate-line comment is inserted, on this line
or on a new line inserted before this line if this line is not blank."
  (interactive)
  (beginning-of-line)
  ;; Recognize existing comments of either kind.
  (cond ((looking-at comment-line-start-skip)
	 (fortran-indent-line))
	((re-search-forward comment-start-skip
			    (save-excursion (end-of-line) (point)) t)
	 (indent-for-comment))
	;; No existing comment.
	;; If side-by-side comments are defined, insert one,
	;; unless line is now blank.
	((and comment-start (not (looking-at "^[ \t]*$")))
	 (end-of-line)
	 (delete-horizontal-space)
	 (indent-to (fortran-comment-hook))
	 (insert comment-start))
	;; Else insert separate-line comment, making a new line if nec.
	(t
	 (if (looking-at "^[ \t]*$")
	     (delete-horizontal-space)
	   (beginning-of-line)
	   (insert "\n")
	   (forward-char -1))
	 (insert comment-line-start)
	 (insert-char (if (stringp fortran-comment-indent-char)
			  (aref fortran-comment-indent-char 0)
			  fortran-comment-indent-char)
		      (- (calculate-fortran-indent) (current-column))))))

(defun fortran-comment-region (beg-region end-region arg)
  "Comments every line in the region.
Puts fortran-comment-region at the beginning of every line in the region. 
BEG-REGION and END-REGION are args which specify the region boundaries. 
With non-nil ARG, uncomments the region."
  (interactive "*r\nP")
  (let ((end-region-mark (make-marker)) (save-point (point-marker)))
    (set-marker end-region-mark end-region)
    (goto-char beg-region)
    (beginning-of-line)
    (if (not arg)			;comment the region
	(progn (insert fortran-comment-region)
	       (while (and  (= (forward-line 1) 0)
			    (< (point) end-region-mark))
		 (insert fortran-comment-region)))
      (let ((com (regexp-quote fortran-comment-region))) ;uncomment the region
	(if (looking-at com)
	    (delete-region (point) (match-end 0)))
	(while (and  (= (forward-line 1) 0)
		     (< (point) end-region-mark))
	  (if (looking-at com)
	      (delete-region (point) (match-end 0))))))
    (goto-char save-point)
    (set-marker end-region-mark nil)
    (set-marker save-point nil)))

(defun fortran-abbrev-start ()
  "Typing \";\\[help-command]\" or \";?\" lists all the fortran abbrevs. 
Any other key combination is executed normally." ;\\[help-command] is just a way to print the value of the variable help-char.
  (interactive)
  (let (c)
    (insert last-command-char)
    (if (or (= (setq c (read-char)) ??)	;insert char if not equal to `?'
	    (= c help-char))
	(fortran-abbrev-help)
      (setq unread-command-char c))))

(defun fortran-abbrev-help ()
  "List the currently defined abbrevs in Fortran mode."
  (interactive)
  (message "Listing abbrev table...")
  (require 'abbrevlist)
  (list-one-abbrev-table fortran-mode-abbrev-table "*Help*")
  (message "Listing abbrev table...done"))

(defun fortran-column-ruler ()
  "Inserts a column ruler momentarily above current line, till next keystroke.
The ruler is defined by the value of fortran-column-ruler.
The key typed is executed unless it is SPC."
  (interactive)
  (momentary-string-display 
   fortran-column-ruler (save-excursion (beginning-of-line) (point))
   nil "Type SPC or any command to erase ruler."))

(defun fortran-window-create ()
  "Makes the window 72 columns wide."
  (interactive)
  (let ((window-min-width 2))
    (split-window-horizontally 73))
  (other-window 1)
  (switch-to-buffer " fortran-window-extra" t)
  (select-window (previous-window)))

(defun fortran-split-line ()
  "Break line at point and insert continuation marker and alignment."
  (interactive)
  (delete-horizontal-space)
  (if (save-excursion (beginning-of-line) (looking-at comment-line-start-skip))
      (insert ?\n comment-line-start ?\  )
      (insert ?\n fortran-continuation-char))
  (fortran-indent-line))

(defun delete-horizontal-regexp (chars)
  "Delete all characters in CHARS around point.
CHARS is like the inside of a [...] in a regular expression
except that ] is never special and \ quotes ^, - or \."
  (interactive "*s")
  (skip-chars-backward chars)
  (delete-region (point) (progn (skip-chars-forward chars) (point))))

(defun fortran-electric-line-number (arg)
  "Self insert, but if part of a Fortran line number indent it automatically.
Auto-indent does not happen if a numeric arg is used."
;; check for overwrite-mode was added to allow the overwrite of numbers
;; which otherwise are mapped to fortran-electric-line-number
;; the call to prefix-numeric-value was added to handle the raw data
;; from the call to interactive. it is unknown why it wasn't there
;; before. (March 88)
  (interactive "P")
  (if (or arg (not fortran-electric-line-number) overwrite-mode)
      (self-insert-command (prefix-numeric-value arg))
    (if (or (save-excursion (re-search-backward "[^ \t0-9]"
						(save-excursion
						  (beginning-of-line)
						  (point))
						t)) ;not a line number
	    (looking-at "[0-9]"))		;within a line number
	(insert last-command-char)
      (skip-chars-backward " \t")
      (insert last-command-char)
      (fortran-indent-line))))

(defun beginning-of-fortran-subprogram ()
  "Moves point to the beginning of the current fortran subprogram."
  (interactive)
  (let ((case-fold-search t))
    (beginning-of-line -1)
    (re-search-backward "^[ \t0-9]*end\\b[ \t]*[^ \t=(a-z]" nil 'move)
    (if (looking-at "^[ \t0-9]*end\\b[ \t]*[^ \t=(a-z]")
	(forward-line 1))))

(defun end-of-fortran-subprogram ()
  "Moves point to the end of the current fortran subprogram."
  (interactive)
  (let ((case-fold-search t))
    (beginning-of-line 2)
    (re-search-forward "^[ \t0-9]*end\\b[ \t]*[^ \t=(a-z]" nil 'move)
    (goto-char (match-beginning 0))
    (forward-line 1)))

(defun mark-fortran-subprogram ()
  "Put mark at end of fortran subprogram, point at beginning. 
The marks are pushed."
  (interactive)
  (end-of-fortran-subprogram)
  (push-mark (point))
  (beginning-of-fortran-subprogram))
  
(defun fortran-previous-statement ()
  "Moves point to beginning of the previous fortran statement.
Returns 'first-statement if that statement is the first
non-comment Fortran statement in the file, and nil otherwise."
  (interactive)
  (let (not-first-statement continue-test)
    (beginning-of-line)
    (setq continue-test
	  (or (looking-at
	        (concat "[ \t]*" (regexp-quote (char-to-string
						 fortran-continuation-char))))
	      (looking-at "     [^ 0\n]")))
    (while (and (setq not-first-statement (= (forward-line -1) 0))
		(or (looking-at comment-line-start-skip)
		    (looking-at "[ \t]*$")
		    (looking-at "     [^ 0\n]")
		    (looking-at (concat "[ \t]*"  comment-start-skip)))))
    (cond ((and continue-test
		(not not-first-statement))
	   (message "Incomplete continuation statement."))
	  (continue-test	
	   (fortran-previous-statement))
	  ((not not-first-statement)
	   'first-statement))))

(defun fortran-next-statement ()
  "Moves point to beginning of the next fortran statement.
 Returns 'last-statement if that statement is the last
 non-comment Fortran statement in the file, and nil otherwise."
  (interactive)
  (let (not-last-statement)
    (beginning-of-line)
    (while (and (setq not-last-statement (= (forward-line 1) 0))
 		(or (looking-at comment-line-start-skip)
 		    (looking-at "[ \t]*$")
 		    (looking-at "     [^ 0\n]")
 		    (looking-at (concat "[ \t]*"  comment-start-skip)))))
    (if (not not-last-statement)
 	'last-statement)))

(defun fortran-indent-line ()
  "Indents current fortran line based on its contents and on previous lines."
  (interactive)
  (let ((cfi (calculate-fortran-indent)))
    (save-excursion
      (beginning-of-line)
      (if (or (not (= cfi (fortran-current-line-indentation)))
	      (and (re-search-forward "^[ \t]*[0-9]+" (+ (point) 4) t)
		   (not (fortran-line-number-indented-correctly-p))))
	  (fortran-indent-to-column cfi)
	(beginning-of-line)
	(if (re-search-forward comment-start-skip
			       (save-excursion (end-of-line) (point)) 'move)
	    (fortran-indent-comment))))
    ;; Never leave point in left margin.
    (if (< (current-column) cfi)
	(move-to-column cfi))))

(defun fortran-electric-tab-carriage-return (arg)
;; added 5/24/88 to map a carriage return through indent handling routines
  (interactive "P")
  (if (not fortran-electric-tab-carriage-return)
     (newline)
     (if (= (current-column) 0)
	 (newline)
     (fortran-indent-line)
     (newline))))

(defun fortran-indent-subprogram ()
  "Properly indents the Fortran subprogram which contains point."
  (interactive)
  (save-excursion
    (mark-fortran-subprogram)
    (message "Indenting subprogram...")
    (indent-region (point) (mark) nil))
  (message "Indenting subprogram...done."))

(defun calculate-fortran-indent ()
  "Calculates the fortran indent column based on previous lines."
  (let (icol first-statement (case-fold-search t))
    (save-excursion
      (setq first-statement (fortran-previous-statement))
      (if first-statement
	  (setq icol fortran-minimum-statement-indent)
	(progn
	  (if (= (point) (point-min))
	      (setq icol fortran-minimum-statement-indent)
	    (setq icol (fortran-current-line-indentation)))
	  (skip-chars-forward " \t0-9")
	  (cond ((looking-at "if[ \t]*(")
		 (if (or (looking-at ".*)[ \t]*then\\b[ \t]*[^ \t(=a-z0-9]")
			 (let (then-test)	;multi-line if-then
			   (while (and (= (forward-line 1) 0) ;search forward for then
				       (looking-at "     [^ 0]")
				       (not (setq then-test (looking-at ".*then\\b[ \t]*[^ \t(=a-z0-9]")))))
			   then-test))
		     (setq icol (+ icol fortran-if-indent))))
		((looking-at "\\(else\\|elseif\\)\\b")
		 (setq icol (+ icol fortran-if-indent)))
		((looking-at "do\\b")
		 (setq icol (+ icol fortran-do-indent)))))))
    (save-excursion
      (beginning-of-line)
      (cond ((looking-at "[ \t]*$"))
	    ((looking-at comment-line-start-skip)
	     (cond ((eq fortran-comment-indent-style 'relative)
		    (setq icol (+ icol fortran-comment-line-column)))
		   ((eq fortran-comment-indent-style 'fixed)
		    (setq icol fortran-comment-line-column))))
	    ((or (looking-at (concat "[ \t]*"
				     (regexp-quote (char-to-string fortran-continuation-char))))
		 (looking-at "     [^ 0\n]"))
	     (setq icol (+ icol fortran-continuation-indent)))
	    (first-statement)
	    ((and fortran-check-all-num-for-matching-do
		  (looking-at "[ \t]*[0-9]+")
		  (fortran-check-for-matching-do))
	     (setq icol (- icol fortran-do-indent)))
	    (t
	     (skip-chars-forward " \t0-9")
	     (cond ((looking-at "end[ \t]*if\\b")
		    (setq icol (- icol fortran-if-indent)))
		   ((looking-at "\\(else\\|elseif\\)\\b")
		    (setq icol (- icol fortran-if-indent)))
		   ((and (looking-at "continue\\b")
			 (fortran-check-for-matching-do))
		    (setq icol (- icol fortran-do-indent)))
		   ((looking-at "end[ \t]*do\\b")
		    (setq icol (- icol fortran-do-indent)))
		   ((and (looking-at "end\\b[ \t]*[^ \t=(a-z]")
			 (not (= icol fortran-minimum-statement-indent)))
 		    (message "Warning: `end' not in column %d.  Probably an unclosed block." fortran-minimum-statement-indent))))))
    (max fortran-minimum-statement-indent icol)))

(defun fortran-current-line-indentation ()
  "Indentation of current line, ignoring Fortran line number or continuation.
This is the column position of the first non-whitespace character
aside from the line number and/or column 5 line-continuation character.
For comment lines, returns indentation of the first
non-indentation text within the comment."
  (save-excursion
    (beginning-of-line)
    (cond ((looking-at comment-line-start-skip)
	   (goto-char (match-end 0))
	   (skip-chars-forward
	     (if (stringp fortran-comment-indent-char)
		 fortran-comment-indent-char
	         (char-to-string fortran-comment-indent-char))))
	  ((looking-at "     [^ 0\n]")
	   (goto-char (match-end 0)))
	  (t
	   ;; Move past line number.
	   (move-to-column 5)))
    ;; Move past whitespace.
    (skip-chars-forward " \t")
    (current-column)))

(defun fortran-indent-to-column (col)
  "Indents current line with spaces to column COL.
notes: 1) A non-zero/non-blank character in column 5 indicates a continuation
          line, and this continuation character is retained on indentation;
       2) If fortran-continuation-char is the first non-whitespace character,
          this is a continuation line;
       3) A non-continuation line which has a number as the first
          non-whitespace character is a numbered line."
  (save-excursion
    (beginning-of-line)
    (if (looking-at comment-line-start-skip)
	(if fortran-comment-indent-style
	    (let ((char (if (stringp fortran-comment-indent-char)
			    (aref fortran-comment-indent-char 0)
			    fortran-comment-indent-char)))
	      (goto-char (match-end 0))
	      (delete-horizontal-regexp (concat " \t" (char-to-string char)))
	      (insert-char char (- col (current-column)))))
      (if (looking-at "     [^ 0\n]")
	  (forward-char 6)
	(delete-horizontal-space)
	;; Put line number in columns 0-4
	;; or put continuation character in column 5.
	(cond ((eobp))
	      ((= (following-char) fortran-continuation-char)
	       (indent-to 5)
	       (forward-char 1))
	      ((looking-at "[0-9]+")
	       (let ((extra-space (- 5 (- (match-end 0) (point)))))
		 (if (< extra-space 0)
		     (message "Warning: line number exceeds 5-digit limit.")
		   (indent-to (min fortran-line-number-indent extra-space))))
	       (skip-chars-forward "0-9"))))
      ;; Point is now after any continuation character or line number.
      ;; Put body of statement where specified.
      (delete-horizontal-space)
      (indent-to col)
      ;; Indent any comment following code on the same line.
      (if (re-search-forward comment-start-skip
			     (save-excursion (end-of-line) (point)) t)
	  (progn (goto-char (match-beginning 0))
		 (if (not (= (current-column) (fortran-comment-hook)))
		     (progn (delete-horizontal-space)
			    (indent-to (fortran-comment-hook)))))))))

(defun fortran-line-number-indented-correctly-p ()
  "Return t if current line's line number is correctly indente.
Do not call if there is no line number."
  (save-excursion
    (beginning-of-line)
    (skip-chars-forward " \t")
    (and (<= (current-column) fortran-line-number-indent)
	 (or (= (current-column) fortran-line-number-indent)
	     (progn (skip-chars-forward "0-9")
		    (= (current-column) 5))))))

(defun fortran-check-for-matching-do ()
  "When called from a numbered statement, returns t
 if matching 'do' is found, and nil otherwise."
  (let (charnum
	(case-fold-search t))
    (save-excursion
      (beginning-of-line)
      (if (looking-at "[ \t]*[0-9]+")
	  (progn
	    (skip-chars-forward " \t")
	    (skip-chars-forward "0") ;skip past leading zeros
	    (setq charnum (buffer-substring (point)
					    (progn (skip-chars-forward "0-9")
						   (point))))
	    (beginning-of-line)
	    (and (re-search-backward
		  (concat "\\(^[ \t0-9]*end\\b[ \t]*[^ \t=(a-z]\\)\\|\\(^[ \t0-9]*do[ \t]*0*"
			  charnum "\\b\\)\\|\\(^[ \t]*0*" charnum "\\b\\)")
		  nil t)
		 (looking-at (concat "^[ \t0-9]*do[ \t]*0*" charnum))))))))

   (setq auto-mode-alist (cons '("\\.F$" . fortran-mode)
				(cons '("\\.html$" . html-mode) 
				auto-mode-alist)))


(put 'downcase-region 'disabled nil)
