# Source availability for the diagram renderer's EPL components

The elkjs portions of the distributed diagram renderer are available under the
Eclipse Public License 2.0. Their upstream source code and build instructions
are available from the elkjs 0.9.3 source release:

https://github.com/kieler/elkjs/tree/a8304cf79fde75bc2ab1a89d28320f53f8637436

The underlying Eclipse Layout Kernel Java sources, including their history,
are available under EPL-2.0 from:

https://github.com/eclipse/elk

The elkjs build at that revision reads those sources from an external `elkRepo`;
its CI selects the upstream master branch and does not record the Java input
commit. This audit does not invent that missing revision or claim a byte-identical
rebuild of the Java-to-JavaScript step. The npm elkjs release itself is pinned by
version and integrity, and the final JavaScript-to-HTML bundling was reproduced.

The runtime source archives identified by that release's build.gradle are linked
below. Their copyright headers and applicable license texts are included alongside
this notice. Eclipse EMF portions retain EPL-1.0 terms, including separately
identified Apache-1.1 code; Xtext/Xtend portions retain EPL-2.0 terms. Google GWT
and Guava portions retain their Apache-2.0 notices.

- org.gwtproject:gwt-user:2.10.0: https://maven-central.storage-download.googleapis.com/maven2/org/gwtproject/gwt-user/2.10.0/gwt-user-2.10.0.jar
- com.google.guava:guava-gwt:31.1-jre: https://maven-central.storage-download.googleapis.com/maven2/com/google/guava/guava-gwt/31.1-jre/guava-gwt-31.1-jre.jar
- com.genmymodel.emf.gwt:emf-common:2.12.4: https://maven-central.storage-download.googleapis.com/maven2/com/genmymodel/emf/gwt/emf-common/2.12.4/emf-common-2.12.4-sources.jar
- com.genmymodel.emf.gwt:emf-ecore:2.12.4: https://maven-central.storage-download.googleapis.com/maven2/com/genmymodel/emf/gwt/emf-ecore/2.12.4/emf-ecore-2.12.4-sources.jar
- org.eclipse.xtext:org.eclipse.xtext.xbase.lib:2.28.0: https://maven-central.storage-download.googleapis.com/maven2/org/eclipse/xtext/org.eclipse.xtext.xbase.lib/2.28.0/org.eclipse.xtext.xbase.lib-2.28.0-sources.jar
- org.eclipse.xtend:org.eclipse.xtend.lib:2.28.0: https://maven-central.storage-download.googleapis.com/maven2/org/eclipse/xtend/org.eclipse.xtend.lib/2.28.0/org.eclipse.xtend.lib-2.28.0-sources.jar
